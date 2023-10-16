## Simple data extraction
import openai

# Read lease.txt
with open('lease.txt') as f:
    lease = f.read()

# Create prompt
q = f'''
You are a text processing agent working with lease agreement document.

Extract specified values from the source text.
Return answer as JSON object with following fields:
- "landlord_name" <string>
- "tenant_name" <string>
- "property_address" <string>
- "monthly_rent_fee" <number>
- "start_date" <string> lease agreement start date

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{lease}
========
'''

# OpenAI call, print result
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[{"role": "user", "content": q}])
c = completion.choices[0].message.content
print(c)
