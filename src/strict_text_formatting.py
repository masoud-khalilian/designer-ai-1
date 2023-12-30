# got this function from https://github.com/tanchongmin/strictjson
import re


def strict_text(api_clinet, system_prompt, user_prompt, output_format, delimiter='###',
                model='gpt-3.5-turbo-1106', temperature=0, num_tries=2, verbose=False):
    ''' Ensures that OpenAI will always adhere to the desired output json format.
    Uses rule-based iterative feedback to ask GPT to self-correct.
    Keeps trying up to num_tries it it does not. Returns empty json if unable to after num_tries iterations.'''

    # start off with no error message
    error_msg = ''

    for i in range(num_tries):
        print('this is the number if tries', i)

        # make the output format keys with a unique identifier
        new_output_format = {}
        for key in output_format.keys():
            new_output_format[f'{delimiter}{key}{delimiter}'] = output_format[key]
        output_format_prompt = f'''\nYou are to output the following in json format: {new_output_format}
You must use "{delimiter}{{key}}{delimiter}" to enclose the each {{key}}.'''

        # Use OpenAI to get a response
        response = api_clinet.chat.completions.create(
            # temperature = temperature,
            model=model,
            messages=[
                {"role": "system", "content": system_prompt + \
                 output_format_prompt + error_msg},
                {"role": "user", "content": str(user_prompt)}
            ]
        )

        # res = response['choices'][0]['message']['content']
        res = response.choices[0].message.content

        if verbose:
            print('System prompt:', system_prompt +
                  output_format_prompt + error_msg)
            print('\nUser prompt:', str(user_prompt))
            print('\nGPT response:', res)

        # try-catch block to ensure output format is adhered to
        try:
            # check key appears for each element in the output
            for key in new_output_format.keys():
                # if output field missing, raise an error
                if key not in res:
                    raise Exception(f"{key} not in json output")

            # if all is good, we then extract out the fields
            # Use regular expressions to extract keys and values
            pattern = fr",*\s*['|\"]{delimiter}([^#]*){delimiter}['|\"]: "

            matches = re.split(pattern, res[1:-1])

            # remove null matches
            my_matches = [match for match in matches if match != '']

            # remove the ' or " from the value matches
            curated_matches = [match[1:-1] if match[0]
                               in '\'"' else match for match in my_matches]

            # create a dictionary
            end_dict = {}
            for i in range(0, len(curated_matches), 2):
                end_dict[curated_matches[i]] = curated_matches[i+1]

            return end_dict

        except Exception as e:
            error_msg = f"\n\nResult: {res}\n\nError message: {str(e)}\nYou must use \"{delimiter}{{key}}{delimiter}\" to enclose the each {{key}}."
            print("An exception occurred:", str(e))
            print("Current invalid json format:", res)

    return {}
