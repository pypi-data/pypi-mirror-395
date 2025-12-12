import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Tag, NavigableString
from anthropic import AnthropicFoundry
from dotenv import load_dotenv
import re
import urllib.parse
import argparse
import json
import subprocess

# Load environment variables from .env file (searches parent directories)
load_dotenv(override=False)

# Lazy client initialization - only create when needed
_client = None

def get_client():
    """Get or create the Anthropic client with proper error handling"""
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing ANTHROPIC_API_KEY environment variable. "
                "Please create a .env file with: ANTHROPIC_API_KEY=your_key_here"
            )
        _client = AnthropicFoundry(
            api_key=api_key,
            base_url=os.getenv("ANTHROPIC_ENDPOINT"),
            timeout=600.0
        )
    return _client


def get_provider_from_url(url):
    parsed_url = urllib.parse.urlparse(url)
    path_segments = parsed_url.path.split('/')
    if 'learn.microsoft.com' in parsed_url.netloc and '/rest/api/' in parsed_url.path:
        return 'azapi'
    try:
        provider_index = path_segments.index('providers')
        if provider_index + 2 < len(path_segments):
            return path_segments[provider_index + 2]
    except ValueError:
        pass
    return None

def get_module_path(url):
    provider = get_provider_from_url(url)
    if not provider:
        raise ValueError("Could not determine provider from URL")

    parsed_url = urllib.parse.urlparse(url)
    path_segments = parsed_url.path.split('/')

    if provider == 'azapi':
        # For Azure REST API URLs, extract resource type from the path
        # Example: .../rest/api/containerregistry/registries/create
        try:
            api_index = path_segments.index('api')
            # The next segment is the service, the one after is the resource type
            if api_index + 2 < len(path_segments):
                service = path_segments[api_index + 1]
                resource_type = path_segments[api_index + 2]
                pascal_case_name = f"{service.capitalize()}{resource_type.capitalize()}"
                module_name = f"Azure.{pascal_case_name}"
                return os.path.join('modules', provider, module_name)
        except ValueError:
            pass
        raise ValueError("Could not extract resource type from Azure REST API URL")

    # Existing logic for Terraform Registry URLs
    resource_name_snake_case = None
    for i, segment in enumerate(path_segments):
        if segment == 'resources' and i + 1 < len(path_segments):
            resource_name_snake_case = path_segments[i+1]
            break

    if not resource_name_snake_case:
        raise ValueError("Could not extract resource name from URL")

    pascal_case_name = ''.join(word.capitalize() for word in resource_name_snake_case.split('_'))
    if provider == 'azurerm':
        module_name = f"Azure.{pascal_case_name}"
    else:
        module_name = pascal_case_name

    return os.path.join('modules', provider, module_name)

async def download_azapi_doc(url: str) -> str:
    print(f"\nFetching AzAPI REST documentation from: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("load")
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Extract msDocs.data.restAPIData JSON
        rest_data_script = await page.evaluate("""
            () => {
                const scripts = Array.from(document.querySelectorAll('script'));
                for (const script of scripts) {
                    const text = script.textContent;
                    if (text.includes('msDocs.data.restAPIData')) {
                        const jsonText = text.split('msDocs.data.restAPIData = ')[1].split(';')[0];
                        return jsonText;
                    }
                }
                return null;
            }
        """)
        await browser.close()

        md_lines = ["## URI Parameters\n"]
        if not rest_data_script:
            raise Exception("Failed to extract msDocs REST data.")

        rest_data = json.loads(rest_data_script)
        for param in rest_data.get("uriParameters", []):
            name = param["name"]
            required = "required" if param.get("isRequired") else "optional"
            typ = param.get("type", "string")
            md_lines.append(f"- **`{name}`** *(type: {typ}, {required})*")

        # Request Body
        md_lines.append("\n## Request Body\n")
        body_section = soup.find("h2", {"id": "request-body"})
        table = body_section.find_next("table") if body_section else None
        if not table:
            md_lines.append("- *(Request body section not found)*")
        else:
            rows = table.find_all("tr")
            if len(rows) <= 1:
                # Only header row, no data
                md_lines.append("- *(Request body table is present but contains no parameters)*")
            else:
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all("td")
                    if len(cols) >= 3:
                        name = cols[0].get_text(strip=True).replace("\n", "").replace("\xa0", " ")
                        typ = cols[1].get_text(strip=True)
                        desc = cols[2].get_text(strip=True).replace("\n", " ")
                        md_lines.append(f"- **`{name}`** *(type: {typ})* – {desc}")

        return "\n".join(md_lines)

def html_to_markdown(elem):
    # Convert HTML element to Markdown recursively with improved formatting
    if elem.name in ['ul', 'ol']:
        return list_to_md(elem)
    if elem.name == 'li':
        return li_to_md(elem)
    if elem.name in ['h3', 'h4', 'h5', 'h6']:
        level = int(elem.name[1])
        return f"{'#' * level} {elem.get_text(strip=True)}"
    if elem.name == 'pre':
        code = elem.get_text('\n', strip=True)
        return f"\n```hcl\n{code}\n```\n"
    if elem.name == 'code':
        return f"`{elem.get_text(strip=True)}`"
    if elem.name == 'p':
        return p_to_md(elem)
    if elem.name == 'div' and 'alert' in elem.get('class', []):
        # Note or warning block - flatten to a single paragraph
        note_type = 'Note' if 'alert-info' in elem.get('class', []) else 'Warning'
        text = flatten_alert(elem)
        return f"> **{note_type}:** {text}"
    if elem.name == 'hr':
        return '\n---\n'
    if elem.name == 'a':
        # Remove anchor references from links but keep brackets for internal links
        href = elem.get('href', '')
        if href.startswith('#'):
            return f"[{elem.get_text(strip=True)}]"
        return f"[{elem.get_text(strip=True)}]({href})"
    # Generic recursive conversion for other tags
    content_parts = []
    for child in elem.children:
        if isinstance(child, Tag):
            content_parts.append(html_to_markdown(child))
        elif isinstance(child, NavigableString):
            s = str(child).strip()
            if s:
                content_parts.append(s)
    return ' '.join(content_parts).strip()

def flatten_alert(alert_elem):
    # Flatten all text and inline code in the alert into a single paragraph
    parts = []
    for child in alert_elem.descendants:
        if isinstance(child, Tag) and child.name == 'code':
            parts.append(f'`{child.get_text(strip=True)}`')
        elif isinstance(child, Tag) and child.name == 'br':
            parts.append(' ')
        elif isinstance(child, NavigableString):
            s = str(child).replace('\n', ' ').strip()
            if s:
                parts.append(s)
    # Remove extra spaces and join
    text = ' '.join(parts)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def list_to_md(ul_elem):
    items = []
    for li in ul_elem.find_all('li', recursive=False):
        items.append(li_to_md(li))
    return '\n'.join(items)

def li_to_md(li_elem):
    # Try to bold and code the argument name and process children recursively
    text_parts = []
    for child in li_elem.children:
        if isinstance(child, Tag) and child.name == 'a' and child.code:
            arg = child.get_text(strip=True)
            href = child.get('href', '')
            if href and not href.startswith('#'):  # Only keep non-anchor links
                text_parts.append(f'**[`{arg}`]({href})**')
            else:
                text_parts.append(f'**[{arg}]**')  # Keep square brackets but remove anchor
        elif isinstance(child, Tag) and child.name == 'code':
            text_parts.append(f'**`{child.get_text(strip=True)}`**')
        elif isinstance(child, NavigableString):
            s = str(child)
            dash_idx = s.find('-')
            if dash_idx > 0:
                arg_part = s[:dash_idx].strip()
                desc_part = s[dash_idx+1:].strip()
                if arg_part:
                    text_parts.append(f'**[{arg_part}]** – {desc_part}')
                else:
                    text_parts.append(desc_part)
            else:
                text_parts.append(s)
        elif isinstance(child, Tag):
            # Recursively convert nested tags within <li>
            text_parts.append(html_to_markdown(child))

    return f'- {" ".join(text_parts).strip()}'

def p_to_md(p_elem):
    # Convert <p> with possible <code> and <a> children recursively
    out_parts = []
    for child in p_elem.children:
        if isinstance(child, Tag) and child.name == 'code':
            out_parts.append(f'`{child.get_text(strip=True)}`')
        elif isinstance(child, Tag) and child.name == 'a':
            label = child.get_text(strip=True)
            href = child.get('href', '')
            if href and not href.startswith('#'):  # Only keep non-anchor links
                out_parts.append(f'[{label}]({href})')
            else:
                out_parts.append(label)
        elif isinstance(child, Tag):
            # Recursively convert nested tags within <p>
            out_parts.append(html_to_markdown(child))
        else:
            out_parts.append(str(child))
    return ' '.join(out_parts).strip()

def fetch_schema_block(provider: str, resource: str):
    import tempfile
    import subprocess
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "main.tf"), "w") as f:
                f.write(f"""
terraform {{
  required_providers {{
    {provider} = {{
      source  = "hashicorp/{provider}"
    }}
  }}
}}

provider "{provider}" {{}}
""")
            
            # Run terraform init
            subprocess.run(["terraform", "init"], cwd=tmpdir, check=True, capture_output=True)
            
            # Run terraform providers schema -json
            result = subprocess.run(
                ["terraform", "providers", "schema", "-json"], 
                cwd=tmpdir, 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            schema = json.loads(result.stdout)
            
            # Navigate to the resource schema
            provider_key = f"registry.terraform.io/hashicorp/{provider}"
            resource_key = f"{provider}_{resource}"
            
            try:
                block = schema["provider_schemas"][provider_key]["resource_schemas"][resource_key]["block"]
                return block
            except KeyError:
                return None
                
    except Exception as e:
        print(f"Error fetching schema: {e}")
        return None

def split_and_save_outputs(gpt_output, module_dir):
    os.makedirs(module_dir, exist_ok=True)
    
    # Split output by headers like ### main.tf
    files = {}
    current_file = None
    lines = gpt_output.split('\n')
    
    for line in lines:
        match = re.match(r'^###\s+(.+)', line)
        if match:
            current_file = match.group(1).strip()
            files[current_file] = []
        elif current_file:
            files[current_file].append(line)
            
    for filename, content_lines in files.items():
        content = '\n'.join(content_lines).strip()
        # Remove markdown code blocks if present
        content = re.sub(r'^```hcl', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'^```', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'```$', '', content, flags=re.IGNORECASE).strip()
        
        with open(os.path.join(module_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)

async def validate_parameter_completeness(module_dir, schema_text, doc_text, url):
    """Check that all parameters from schema/documentation are included in the generated module"""
    print(f"\n🔍 Checking parameter completeness...")
    
    try:
        # Read the generated variables.tf
        variables_path = os.path.join(module_dir, 'variables.tf')
        if not os.path.exists(variables_path):
            print("⚠️ variables.tf not found, skipping completeness check")
            return True, None
        
        with open(variables_path, 'r', encoding='utf-8') as f:
            variables_content = f.read()
        
        # Use AI to compare generated variables against schema
        client = get_client()
        deployment = "claude-sonnet-4-5"
        
        system_prompt = (
            f"You are validating a Terraform module for parameter completeness.\n"
            f"Compare the generated variables.tf against the JSON schema/documentation to identify missing parameters.\n\n"
            f"## Schema JSON:\n{schema_text}\n\n"
            f"## Documentation:\n{doc_text}\n\n"
            f"## Generated variables.tf:\n{variables_content}\n\n"
            f"TASK:\n"
            f"1. List ALL parameters/arguments from the schema/documentation\n"
            f"2. Check which ones are present in variables.tf\n"
            f"3. Identify any MISSING parameters\n\n"
            f"Output format:\n"
            f"If ALL parameters are present: output exactly 'COMPLETE'\n"
            f"If parameters are missing: output 'INCOMPLETE' followed by a list of missing parameters with their types and descriptions.\n"
        )
        
        user_prompt = "Check if all parameters from the schema are present in the generated variables.tf"
        
        message = client.messages.create(
            model=deployment,
            messages=[
                {"role": "user", "content": system_prompt + "\n\n" + user_prompt}
            ],
            max_tokens=5000
        )
        
        result = message.content[0].text.strip() if message.content else "UNKNOWN"
        
        if "COMPLETE" in result:
            print("✅ All parameters from schema are present in the module")
            return True, None
        else:
            print("⚠️ Some parameters are missing from the generated module:")
            print(result)
            return False, result
    
    except Exception as e:
        print(f"⚠️ Error during completeness check: {e}")
        # Don't fail the whole process if this check fails
        return True, None

def validate_terraform_module(module_dir, context="Module"):
    """Run terraform init and validate on the generated module"""
    print(f"\n🔧 Validating Terraform {context} in {module_dir}...")
    
    try:
        # Run terraform init
        print("Running terraform init...")
        init_result = subprocess.run(
            ["terraform", "init", "-input=false", "-no-color"],
            cwd=module_dir,
            capture_output=True,
            text=True,
            check=False
        )
        
        if init_result.returncode != 0:
            print(f"❌ terraform init failed:")
            print(f"STDOUT: {init_result.stdout}")
            print(f"STDERR: {init_result.stderr}")
            return False, f"terraform init failed:\nSTDOUT: {init_result.stdout}\nSTDERR: {init_result.stderr}"
        else:
            print("✅ terraform init successful")
        
        # Run terraform validate
        print("Running terraform validate...")
        validate_result = subprocess.run(
            ["terraform", "validate", "-no-color"],
            cwd=module_dir,
            capture_output=True,
            text=True,
            check=False
        )
        
        if validate_result.returncode != 0:
            print(f"❌ terraform validate failed:")
            print(f"STDOUT: {validate_result.stdout}")
            print(f"STDERR: {validate_result.stderr}")
            error_output = f"terraform validate failed:\nSTDOUT: {validate_result.stdout}\nSTDERR: {validate_result.stderr}"
            return False, error_output
        else:
            print("✅ terraform validate successful")
            print(f"🎉 {context} validation completed successfully!")
            return True, None
            
    except FileNotFoundError:
        print("❌ Error: terraform command not found. Please ensure Terraform is installed and in your PATH.")
        return False, "terraform command not found"
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False, str(e)

async def generate_examples_with_gpt(module_dir, url, schema_text, doc_text=""):
    """Generate examples folder using AI based on the module files and schema"""
    print(f"\n📁 Generating examples folder with AI for {module_dir}...")
    
    try:
        # Read the generated module files
        module_files = {}
        for filename in ['main.tf', 'variables.tf', 'outputs.tf']:
            file_path = os.path.join(module_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    module_files[filename] = f.read()
        
        # Extract provider and resource info
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.split("/")
        
        if get_provider_from_url(url) == "azapi":
            try:
                api_index = path_parts.index('api')
                service = path_parts[api_index + 1]
                resource = path_parts[api_index + 2]
                provider = "azapi"
            except:
                provider = "azapi"
                resource = "resource"
        else:
            try:
                provider = path_parts[path_parts.index("providers") + 2]
                resource = path_parts[path_parts.index("resources") + 1]
            except:
                provider = "unknown"
                resource = "resource"
        
        # Create AI prompt for examples generation
        system_prompt = (
            f"You are creating example usage files for a Terraform module `{provider}_{resource}`.\n"
            f"Below are the generated module files and the provider schema.\n"
            f"Create complete example usage in an 'examples' folder with:\n"
            f"1. main.tf - Complete working example that calls the module with all parameters\n"
            f"2. variables.tf - Variable definitions for the example (same as module but for example usage)\n"
            f"3. terraform.tfvars - Example values for all variables\n\n"
            f"## Module Files:\n"
        )
        
        for filename, content in module_files.items():
            system_prompt += f"### {filename}\n```hcl\n{content}\n```\n\n"
        
        system_prompt += (
            f"## Provider Schema:\n{schema_text}\n\n"
            f"## Documentation:\n{doc_text}\n\n"
            f"Generate realistic example values. For required variables, provide actual values in terraform.tfvars.\n"
            f"For optional variables, provide commented examples in terraform.tfvars.\n"
            f"The main.tf should call the module using source = \"..\" (parent directory).\n"
            f"Output the files with these headers exactly:\n"
            f"### examples/main.tf\n...\n### examples/variables.tf\n...\n### examples/terraform.tfvars\n...\n"
        )
        
        client = get_client()
        deployment = "claude-sonnet-4-5"
        
        message = client.messages.create(
            model=deployment,
            messages=[
                {"role": "user", "content": system_prompt + "\n\nGenerate the example files for this Terraform module."}
            ],
            max_tokens=30000
        )
        
        if message.content:
            examples_output = message.content[0].text.strip()
            return save_examples_output(examples_output, module_dir)
        else:
            print("❌ AI did not return examples output.")
            return None
            
    except Exception as e:
        print(f"❌ Error generating examples with AI: {e}")
        return None

def save_examples_output(examples_output, module_dir):
    """Parse and save the AI-generated examples output"""
    examples_dir = os.path.join(module_dir, 'examples')
    os.makedirs(examples_dir, exist_ok=True)
    
    sections = {
        'main.tf': '',
        'variables.tf': '',
        'terraform.tfvars': ''
    }
    
    current_section = None
    code_lines = []
    
    for line in examples_output.splitlines():
        # Look for headers like "### examples/main.tf"
        header_match = re.match(r'^#+\s*examples/(main\.tf|variables\.tf|terraform\.tfvars)', line.strip().lower())
        if header_match:
            if current_section and code_lines:
                content = '\n'.join(code_lines).strip()
                # Clean up code blocks
                content = re.sub(r'^```hcl', '', content, flags=re.IGNORECASE).strip()
                content = re.sub(r'^```', '', content, flags=re.IGNORECASE).strip()
                content = re.sub(r'```$', '', content, flags=re.IGNORECASE).strip()
                sections[current_section] = content
            
            current_section = header_match.group(1)
            code_lines = []
        elif current_section:
            code_lines.append(line)
    
    # Handle the last section
    if current_section and code_lines:
        content = '\n'.join(code_lines).strip()
        content = re.sub(r'^```hcl', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'^```', '', content, flags=re.IGNORECASE).strip()
        content = re.sub(r'```$', '', content, flags=re.IGNORECASE).strip()
        sections[current_section] = content
    
    # Save the files
    print(f"\n💾 Saving examples to {examples_dir}/...\n")
    for filename, content in sections.items():
        if content:
            file_path = os.path.join(examples_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Created {file_path} ({len(content)} characters)')
        else:
            print(f'⚠️ Warning: {filename} is empty or missing in AI output')
    
    print(f'✅ Examples folder created successfully!')
    return examples_dir

async def fix_examples_with_gpt(module_dir, url, schema_text, doc_text, error_context):
    """Fix examples validation errors using AI"""
    print(f"\n🔧 Fixing examples validation errors with AI...")
    
    try:
        # Read the current module files and examples files
        module_files = {}
        examples_files = {}
        
        # Read module files
        for filename in ['main.tf', 'variables.tf', 'outputs.tf']:
            file_path = os.path.join(module_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    module_files[filename] = f.read()
        
        # Read examples files
        examples_dir = os.path.join(module_dir, 'examples')
        for filename in ['main.tf', 'variables.tf', 'terraform.tfvars']:
            file_path = os.path.join(examples_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    examples_files[filename] = f.read()
        
        # Extract provider and resource info
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.split("/")
        
        if get_provider_from_url(url) == "azapi":
            try:
                api_index = path_parts.index('api')
                service = path_parts[api_index + 1]
                resource = path_parts[api_index + 2]
                provider = "azapi"
            except:
                provider = "azapi"
                resource = "resource"
        else:
            try:
                provider = path_parts[path_parts.index("providers") + 2]
                resource = path_parts[path_parts.index("resources") + 1]
            except:
                provider = "unknown"
                resource = "resource"
        
        # Create AI prompt for fixing examples
        system_prompt = (
            f"You are fixing example usage files for a Terraform module `{provider}_{resource}` that have validation errors.\n"
            f"Below are the module files, current examples files, provider schema, and validation errors.\n"
            f"Fix the validation errors in the examples while maintaining proper usage of the module.\n\n"
            f"## Module Files:\n"
        )
        
        for filename, content in module_files.items():
            system_prompt += f"### {filename}\n```hcl\n{content}\n```\n\n"
        
        system_prompt += f"## Current Examples Files:\n"
        for filename, content in examples_files.items():
            system_prompt += f"### examples/{filename}\n```hcl\n{content}\n```\n\n"
        
        system_prompt += (
            f"## Provider Schema:\n{schema_text}\n\n"
            f"## Documentation:\n{doc_text}\n\n"
            f"## Terraform Validation Errors:\n{error_context}\n\n"
            f"Fix these validation errors in the examples. The examples should properly call the module.\n"
            f"Output the corrected example files with these headers exactly:\n"
            f"### examples/main.tf\n...\n### examples/variables.tf\n...\n### examples/terraform.tfvars\n...\n"
        )
        
        client = get_client()
        deployment = "claude-sonnet-4-5"
        
        message = client.messages.create(
            model=deployment,
            system=system_prompt,
            messages=[
                {"role": "user", "content": "Generate the example files for this Terraform module."}
            ],
            max_tokens=30000,
            temperature=1,
        )
        
        if message.content:
            return message.content[0].text.strip()
        else:
            print("❌ AI did not return fixed examples output.")
            return None
            
    except Exception as e:
        print(f"❌ Error fixing examples with AI: {e}")
        return None

async def create_examples_with_ai(module_path, url):
    """Helper function to create examples using AI with proper schema context"""
    try:
        # Extract provider and resource info to get schema
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.split("/")
        
        if get_provider_from_url(url) == "azapi":
            # For azapi, use documentation
            doc_text = await download_azapi_doc(url)
            schema_text = "Schema not available for AzAPI."
        else:
            try:
                provider = path_parts[path_parts.index("providers") + 2]
                resource = path_parts[path_parts.index("resources") + 1]
                schema_block = fetch_schema_block(provider, resource)
                schema_text = json.dumps(schema_block, indent=2) if schema_block else "Schema not available."
                doc_text = ""
            except Exception as e:
                print(f"⚠️ Could not extract provider/resource info: {e}")
                schema_text = "Schema not available."
                doc_text = ""
        
        # Generate examples with AI
        examples_dir = await generate_examples_with_gpt(module_path, url, schema_text, doc_text)
        
        # Validate the examples folder if it was created successfully
        if examples_dir:
            print(f"\n🔧 Validating examples in {examples_dir}...")
            examples_validation, examples_error = validate_terraform_module(examples_dir, context="Examples")
            if examples_validation:
                print("🎉 Examples validation successful!")
            else:
                print(f"⚠️ Examples validation failed. Attempting to fix with AI...")
                
                # Keep trying to fix with AI until successful or max attempts reached
                max_attempts = 5
                current_error = examples_error
                
                for attempt in range(1, max_attempts + 1):
                    print(f"\n🔧 AI fix attempt {attempt}/{max_attempts}...")
                    fixed_examples = await fix_examples_with_gpt(module_path, url, schema_text, doc_text, current_error)
                    
                    if fixed_examples:
                        print(f"\n💾 Saving fixed examples (attempt {attempt})...")
                        save_examples_output(fixed_examples, module_path)
                        
                        # Re-validate examples
                        print(f"\n🔧 Re-validating fixed examples (attempt {attempt})...")
                        validation_success, validation_error = validate_terraform_module(examples_dir, context="Examples")
                        
                        if validation_success:
                            print(f"\n🎉 Examples successfully fixed and validated on attempt {attempt}!")
                            break
                        else:
                            print(f"\n⚠️ Attempt {attempt} still has validation errors:")
                            print(validation_error)
                            current_error = validation_error
                            
                            if attempt == max_attempts:
                                print(f"\n❌ Failed to fix examples after {max_attempts} attempts.")
                                print("Final errors:")
                                print(validation_error)
                            else:
                                print(f"Trying again with attempt {attempt + 1}...")
                    else:
                        print(f"❌ AI could not generate fixed examples on attempt {attempt}.")
                        if attempt == max_attempts:
                            print(f"\n❌ Failed to generate fixed examples after {max_attempts} attempts.")
        
    except Exception as e:
        print(f"❌ Error creating examples: {e}")

async def generate_module_with_gpt(doc_text, azapi_mode=False, url=None, error_context=None):
    try:
        client = get_client()
        deployment = "claude-sonnet-4-5"

        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.split("/")

        if get_provider_from_url(url) == "azapi":
            try:
                api_index = path_parts.index('api')
                service = path_parts[api_index + 1]
                resource = path_parts[api_index + 2]
                provider = "azapi"
            except Exception as e:
                print(f"❌ Error: Could not extract service/resource from Azure REST API URL '{url}'. Please check the URL format. ({e})")
                return None
            # For azapi, use documentation parsing
            doc_text = await download_azapi_doc(url)
            schema_text = "Schema not available."
            print("\n===== PARSED AZAPI DOCUMENTATION =====\n")
            print(doc_text)
            print("\n===== END PARSED AZAPI DOCUMENTATION =====\n")
        else:
            try:
                provider = path_parts[path_parts.index("providers") + 2]
                resource = path_parts[path_parts.index("resources") + 1]
            except Exception as e:
                print(f"❌ Error: Could not extract provider/resource from URL '{url}'. Please check the URL format. ({e})")
                return None
            schema_block = fetch_schema_block(provider, resource)
            schema_text = json.dumps(schema_block, indent=2) if schema_block else "Schema not available."
            doc_text = ""
            print("\n===== PROVIDER SCHEMA JSON =====\n")
            print(schema_text)
            print("\n===== END PROVIDER SCHEMA JSON =====\n")

        if error_context:
            # This is a fix attempt
            system_prompt = (
                f"You are fixing a Terraform module for resource `{provider}_{resource}` that has validation errors.\n"
                f"Below is the Terraform provider **schema** and the validation errors.\n"
                f"Check the JSON schema and fix these errors. Only use arguments and blocks defined in the schema.\n\n"
                f"## Schema JSON:\n{schema_text}\n\n"
                f"## Documentation:\n{doc_text}\n\n"
                f"## Terraform Validation Errors:\n{error_context}\n\n"
                f"⚠️ CRITICAL MANDATORY RULES - FOLLOW EXACTLY:\n"
                f"1. Look for 'block_types' in schema JSON - EVERY entry there MUST be a dynamic block\n"
                f"2. In documentation: any text matching 'The <name> block supports:' means <name> MUST be dynamic\n"
                f"3. ANY parameter with sub-attributes/nested structure MUST be a dynamic block\n"
                f"4. NEVER assign blocks directly (block_name = var.block_name is ALWAYS WRONG)\n"
                f"5. Use: dynamic \"block_name\" {{ for_each = ... content {{ ... }} }}\n"
                f"6. Nested blocks inside blocks also need nested dynamic blocks\n\n"
                f"HOW TO IDENTIFY BLOCKS NEEDING DYNAMIC:\n"
                f"- Schema has 'block_types' field with the block name\n"
                f"- Documentation says 'The X block supports the following:'\n"
                f"- Parameter has multiple sub-fields (e.g., 'enabled', 'key_id', etc.)\n"
                f"- Block can appear 0-1 times (optional) or 0-many times (list)\n\n"
                f"PATTERN for optional block (0-1 occurrences):\n"
                f"  dynamic \"block_name\" {{\n"
                f"    for_each = var.block_name != null ? [var.block_name] : []\n"
                f"    content {{\n"
                f"      field1 = block_name.value.field1\n"
                f"      field2 = lookup(block_name.value, \"field2\", null)\n"
                f"    }}\n"
                f"  }}\n\n"
                f"PATTERN for list blocks (0-many occurrences):\n"
                f"  dynamic \"block_name\" {{\n"
                f"    for_each = var.block_name\n"
                f"    content {{\n"
                f"      field1 = block_name.value.field1\n"
                f"      field2 = lookup(block_name.value, \"field2\", default_value)\n"
                f"    }}\n"
                f"  }}\n\n"
                f"PATTERN for nested blocks (block inside block):\n"
                f"  dynamic \"outer_block\" {{\n"
                f"    for_each = var.outer_block != null ? [var.outer_block] : []\n"
                f"    content {{\n"
                f"      simple_field = outer_block.value.simple_field\n"
                f"      \n"
                f"      dynamic \"inner_block\" {{\n"
                f"        for_each = lookup(outer_block.value, \"inner_block\", [])\n"
                f"        content {{\n"
                f"          inner_field = inner_block.value.inner_field\n"
                f"        }}\n"
                f"      }}\n"
                f"    }}\n"
                f"  }}\n\n"
                f"❌ ABSOLUTELY FORBIDDEN - These patterns WILL FAIL:\n"
                f"  block_name = var.block_name        # WRONG - must be dynamic\n"
                f"  nested_object = var.nested_object  # WRONG - must be dynamic\n\n"
                f"Output the corrected files below. No explanations. Use these headers exactly:\n"
                f"For variables make sure to use the correct type and default value if available.\n"
                f"If the parameter is required, dont add a default value and if the parameter is optional, add a default value.\n"
                f"### main.tf\n...\n### variables.tf\n...\n### outputs.tf\n...\n"
            )
            user_prompt = "Check the JSON schema and fix these errors in the Terraform module."
        else:
            # This is initial generation
            system_prompt = (
                f"You are generating a Terraform module for resource `{provider}_{resource}`.\n"
                f"Below is the Terraform provider **schema** (if available) and documentation.\n"
                f"Only use arguments and blocks defined in the schema or documentation.\n\n"
                f"## Schema JSON:\n{schema_text}\n\n"
                f"## Documentation:\n{doc_text}\n\n"
                f"⚠️ CRITICAL MANDATORY RULES - FOLLOW EXACTLY:\n"
                f"1. Check 'block_types' in schema JSON - EVERY entry MUST be a dynamic block\n"
                f"2. In docs: any line 'The <name> block supports the following:' means <name> is a block\n"
                f"3. If a parameter has ANY nested parameters/sub-attributes, use dynamic block\n"
                f"4. NEVER assign blocks directly (block_name = var.block_name is FORBIDDEN)\n"
                f"5. For optional blocks: for_each = var.X != null ? [var.X] : []\n"
                f"6. For list blocks: for_each = var.X\n"
                f"7. Blocks inside blocks also need nested dynamic syntax\n\n"
                f"HOW TO IDENTIFY BLOCKS:\n"
                f"- Schema 'block_types' lists all blocks for this resource\n"
                f"- Documentation has sections titled 'The X block supports:'\n"
                f"- Any parameter with multiple sub-fields is a block\n"
                f"- Check if parameter can appear 0-1 times (optional) or 0-many (list)\n\n"
                f"CORRECT pattern for optional block:\n"
                f"  dynamic \"block_name\" {{\n"
                f"    for_each = var.block_name != null ? [var.block_name] : []\n"
                f"    content {{\n"
                f"      attribute1 = block_name.value.attribute1\n"
                f"      attribute2 = lookup(block_name.value, \"attribute2\", null)\n"
                f"    }}\n"
                f"  }}\n\n"
                f"CORRECT pattern for list blocks:\n"
                f"  dynamic \"block_name\" {{\n"
                f"    for_each = var.block_name\n"
                f"    content {{\n"
                f"      required_field = block_name.value.required_field\n"
                f"      optional_field = lookup(block_name.value, \"optional_field\", default)\n"
                f"    }}\n"
                f"  }}\n\n"
                f"CORRECT pattern for nested blocks:\n"
                f"  dynamic \"outer\" {{\n"
                f"    for_each = var.outer != null ? [var.outer] : []\n"
                f"    content {{\n"
                f"      simple_attr = outer.value.simple_attr\n"
                f"      \n"
                f"      dynamic \"inner\" {{\n"
                f"        for_each = lookup(outer.value, \"inner\", [])\n"
                f"        content {{\n"
                f"          inner_attr = inner.value.inner_attr\n"
                f"        }}\n"
                f"      }}\n"
                f"    }}\n"
                f"  }}\n\n"
                f"❌ ABSOLUTELY FORBIDDEN - Will cause validation errors:\n"
                f"  any_block = var.any_block  # FORBIDDEN - must be dynamic{{}}\n\n"
                f"Output files below. No explanations. Use these headers exactly:\n"
                f"For variables make sure to use the correct type and default value if available.\n"
                f"If a block has multiple arguments, make sure to use the correct type.\n" 
                f"If the parameter is required, dont add a default value and if the parameter is optional, add a default value.\n"
                f"### main.tf\n...\n### variables.tf\n...\n### outputs.tf\n...\n"
            )
            user_prompt = "Generate the Terraform module now."

        message = client.messages.create(
            model=deployment,
            messages=[
                {"role": "user", "content": system_prompt + "\n\n" + user_prompt}
            ],
            max_tokens=30000
        )
        return message.content[0].text.strip() if message.content else None
    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return None

async def main():
    try:
        parser = argparse.ArgumentParser(description="Generate Terraform modules from documentation.")
        parser.add_argument('--url', type=str, help='Direct URL to the Terraform resource documentation.')
        parser.add_argument('--generate', action='store_true', help='Generate Terraform files using AI after downloading documentation.')
        args = parser.parse_args()
        if args.url:
            url = args.url
        else:
            url = input("🔗 Enter Terraform resource URL: ").strip()
        if not url:
            raise ValueError("URL cannot be empty")
        module_path = get_module_path(url)
        if args.generate:
            print("\n⚡ Generating Terraform files with AI...\n")
            azapi_mode = get_provider_from_url(url) == "azapi"
            gpt_output = await generate_module_with_gpt("", azapi_mode=azapi_mode, url=url)
            if gpt_output:
                split_and_save_outputs(gpt_output, module_path)
                print("\n🎉 Terraform files generated and saved!")
                
                # Get schema and doc for completeness check
                parsed = urllib.parse.urlparse(url)
                path_parts = parsed.path.split("/")
                azapi_mode = get_provider_from_url(url) == "azapi"
                
                if azapi_mode:
                    doc_text = await download_azapi_doc(url)
                    schema_text = "Schema not available for AzAPI."
                else:
                    try:
                        provider = path_parts[path_parts.index("providers") + 2]
                        resource = path_parts[path_parts.index("resources") + 1]
                        schema_block = fetch_schema_block(provider, resource)
                        schema_text = json.dumps(schema_block, indent=2) if schema_block else "Schema not available."
                        doc_text = ""
                    except:
                        schema_text = "Schema not available."
                        doc_text = ""
                
                # Check parameter completeness
                completeness_ok, missing_params = await validate_parameter_completeness(module_path, schema_text, doc_text, url)
                
                if not completeness_ok:
                    print("\n⚠️ Module is missing some parameters. Attempting to regenerate with AI...")
                    
                    # Try up to 5 times to get complete parameters
                    max_completeness_attempts = 5
                    current_missing = missing_params
                    
                    for attempt in range(1, max_completeness_attempts + 1):
                        print(f"\n🔧 Completeness fix attempt {attempt}/{max_completeness_attempts}...")
                        
                        # Create error context for missing parameters
                        completeness_error = f"MISSING PARAMETERS:\n{current_missing}\n\nPlease add ALL missing parameters to the module."
                        
                        # Regenerate with completeness feedback
                        fixed_output = await generate_module_with_gpt("", azapi_mode=azapi_mode, url=url, error_context=completeness_error)
                        
                        if fixed_output:
                            split_and_save_outputs(fixed_output, module_path)
                            print(f"\n💾 Module regenerated (attempt {attempt})...")
                            
                            # Re-check completeness
                            completeness_ok, current_missing = await validate_parameter_completeness(module_path, schema_text, doc_text, url)
                            
                            if completeness_ok:
                                print(f"\n🎉 All parameters added successfully on attempt {attempt}!")
                                break
                            else:
                                print(f"\n⚠️ Attempt {attempt} still missing some parameters:")
                                print(current_missing)
                                
                                if attempt == max_completeness_attempts:
                                    print(f"\n❌ Failed to add all parameters after {max_completeness_attempts} attempts.")
                                    print("Proceeding with validation anyway...")
                                else:
                                    print(f"Trying again with attempt {attempt + 1}...")
                        else:
                            print(f"❌ AI did not return output on attempt {attempt}.")
                            if attempt == max_completeness_attempts:
                                print(f"\n❌ Failed to regenerate after {max_completeness_attempts} attempts.")
                
                # Validate the generated module
                validation_success, error_output = validate_terraform_module(module_path)
                if not validation_success:
                    print("\n⚠️ Module validation failed. Attempting to fix errors with AI...")
                    
                    # Keep trying to fix with AI until successful or max attempts reached
                    max_attempts = 5
                    current_error = error_output
                    module_fixed = False
                    
                    for attempt in range(1, max_attempts + 1):
                        print(f"\n🔧 AI fix attempt {attempt}/{max_attempts}...")
                        fixed_output = await generate_module_with_gpt("", azapi_mode=azapi_mode, url=url, error_context=current_error)
                        
                        if fixed_output:
                            print(f"\n💾 Saving fixed files (attempt {attempt})...")
                            split_and_save_outputs(fixed_output, module_path)
                            
                            # Re-validate module
                            print(f"\n🔧 Re-validating fixed module (attempt {attempt})...")
                            validation_success, validation_error = validate_terraform_module(module_path)
                            
                            if validation_success:
                                print(f"\n🎉 Module successfully fixed and validated on attempt {attempt}!")
                                module_fixed = True
                                break
                            else:
                                print(f"\n⚠️ Attempt {attempt} still has validation errors:")
                                print(validation_error)
                                current_error = validation_error
                                
                                if attempt == max_attempts:
                                    print(f"\n❌ Failed to fix module after {max_attempts} attempts.")
                                    print("Final errors:")
                                    print(validation_error)
                                else:
                                    print(f"Trying again with attempt {attempt + 1}...")
                        else:
                            print(f"❌ AI could not generate fixed module on attempt {attempt}.")
                            if attempt == max_attempts:
                                print(f"\n❌ Failed to generate fixed module after {max_attempts} attempts.")
                    
                    # Create examples only if module was successfully fixed
                    if module_fixed:
                        await create_examples_with_ai(module_path, url)
                else:
                    # Initial validation was successful
                    await create_examples_with_ai(module_path, url)
            else:
                print("❌ AI did not return any output.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
