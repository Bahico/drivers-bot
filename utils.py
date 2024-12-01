import re


def mask_uzbek_phone_numbers(text):
    # Regex pattern for Uzbek phone numbers
    uzbek_phone_pattern = (r'\b(\+998[-.\s]?|998[-.\s]?|8[-.\s]?)?(90|91|93|94|95|97|98|99|33|88|77)[-.\s]?(\d{3})['
                           r'-.\s]?(\d{2})[-.\s]?(\d{2})\b')

    # Function to mask the identified phone number
    def mask_match(match):
        full_number = match.group(0)
        if len(full_number) == 9:
            masked = full_number[:-4] + '*' * 4
        else:
            masked = full_number[:-5] + '*' * 5

        return masked

    # Replace phone numbers with their masked version
    masked_text = re.sub(uzbek_phone_pattern, mask_match, text)
    return masked_text
