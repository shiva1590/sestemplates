import os
import boto3
import subprocess
import json


# Create Boto3 session using environment variables
session = boto3.Session(
          aws_access_key_id="AKIA3KVEPMYVOZQSV6BB",
          aws_secret_access_key="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",
          region_name="us-east-1"  # Optional
          )

# Create SES client
client = session.client('ses')
print(client.list_templates())
# Get a list of all templates
templates = client.list_templates()['TemplatesMetadata']

# Loop through each template name
for template in templates:
    template_name = template['Name']
    # Get template content from SES
    response = client.get_template(TemplateName=template_name)
    print(response)
    template_json = json.dumps(response['Template'])

    # Save template to file using a descriptive filename
    with open(f"{template_name}.json", "w") as f:
        f.write(template_json)

    # Check for changes and add to PR if needed
        diff_command = f"git diff --unified=0 {template_name}.json"
        diff_output = subprocess.run(diff_command, shell=True, capture_output=True, text=True)
        if diff_output.returncode == 0:
            print(f"Template '{template_name}' unchanged. Skipping update.")
        else:
            print(f"Changes detected in '{template_name}'. Adding to PR.")
            add_command = f"git add {template_name}.json"
            subprocess.run(add_command, shell=True)

# Commit changes, push to repository, and create Pull Request
subprocess.run("git commit -m 'Update all SES templates from API'", shell=True)
subprocess.run("git push origin main", shell=True)
subprocess.run("gh pr create", shell=True)
