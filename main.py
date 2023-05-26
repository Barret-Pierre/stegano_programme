from numpy import array
from PIL import Image


# CONVERT IMAGE INTO PIXEL ARRAY AND VERIFY IF THE MESSAGE COULD BE ENCODE
def convert_image_to_pixel_array(image_name):
    image = Image.open(image_name)
    data = array(image)
    return data


# CONVERT MESSAGE INPUT INTO BINARY
def convert_messsage_binary(message):
    binary_message = ""
    for charac in message:
        binary_charac = bin(ord(charac))[2:].rjust(8, "0")
        binary_message += binary_charac
    return binary_message


# CONVERT MESSAGE INPUT LENGTH INTO BINARY (return 2 octets)
def convert_messsage_length_binary(message):
    message_length = len(message)
    return bin(message_length)[2:].rjust(16, "0")


# PREPARE MESSAGE TO HIDE
def prepare_message(message):
    binary_message_length = convert_messsage_length_binary(message)
    binary_message = convert_messsage_binary(message)
    # Concat binary_message_length and binary_message
    return binary_message_length + binary_message


# CONVERT PIXEL RGB VALUE INTO BINARY (return 1 octet)
def convert_pixel_value_binary(pixel_value):
    return bin(pixel_value)[2:].rjust(8, "0")


# MODIFY THE LEAST SIGNIFICANT BIT
def modify_lsb(pixel_value, message_bit):
    pixel_value_binary = convert_pixel_value_binary(pixel_value)
    array = list(pixel_value_binary)
    array[7] = message_bit
    return int("".join(array), 2)


# EXTRACT THE LEAST SIGNIFICANT BIT
def extract_lsb(pixel_value):
    pixel_value_binary = convert_pixel_value_binary(pixel_value)
    return pixel_value_binary[7]


# DECODE THE MESSAGE LENGTH
def decode_message_length(pixel_array):
    message_length_octet = ""
    row = 0
    pixel = 0
    rgb = 0
    for x in range(16):
        # extract pixel value in binary
        pixel_value_binary = extract_lsb(pixel_array[row][pixel][rgb])
        message_length_octet += pixel_value_binary
        # Past to the next pixel value
        rgb += 1
        if rgb >= 3:
            # Past to the next pixel
            rgb = 0
            pixel += 1
        if pixel >= len(pixel_array[0]):
            # Past to the next pixel
            pixel = 0
            row += 1

    return int(message_length_octet, 2) * 8


# DECODE BINARY MESSAGE HIDE
def decode_message(hide_message_binary):
    hide_message_string = ""
    for x in range(0, len(hide_message_binary), 8):
        hide_message_string += chr(int(hide_message_binary[x : x + 8], 2))
    return hide_message_string


# ENCODE THE MESSAGE INTO THE IMAGE
def encode(message, image_name):
    message_prepared = prepare_message(message)
    # print(message_prepared)
    # Get the image and verify if the message could be encode
    image = Image.open(image_name)
    encoding_dimension = image.width * image.height * 3
    if encoding_dimension < len(message_prepared):
        return print("Encode impossible, your message is too long !")
    else:
        # Convert image into array
        pixel_array = array(image)
        row = 0
        pixel = 0
        rgb = 0
        for x in range(len(message_prepared)):
            # Insert bit of message in pixel value binary
            # print("BEFORE", pixel_array[row][pixel][rgb])
            new_pixel_value = modify_lsb(
                pixel_array[row][pixel][rgb], message_prepared[x]
            )
            # print("AFTER", modify_lsb(pixel_array[row][pixel][rgb], message_prepared[x]))
            # Insert pixel value modified in the pixel array
            pixel_array[row][pixel][rgb] = new_pixel_value

            # Past to the next pixel value
            rgb += 1
            if rgb >= 3:
                # Past to the next pixel
                rgb = 0
                pixel += 1
            if pixel >= len(pixel_array[0]):
                # Past to the next pixel
                pixel = 0
                row += 1

        # creating image object of
        # above array
        image = Image.fromarray(pixel_array)

        # saving the final output
        # as a PNG file
        image.save("SECRET.png")
        return print("Successfull encoded in SECRET.png")


# DECODE THE MESSAGE
def decode(image_name):
    image = Image.open(image_name)
    pixel_array = array(image)
    message_length_bits = decode_message_length(pixel_array)
    hide_message = ""
    row = 0
    pixel = 0
    rgb = 0
    for x in range(16 + message_length_bits):
        # extract pixel value in binary
        pixel_value_binary = extract_lsb(pixel_array[row][pixel][rgb])
        hide_message += pixel_value_binary
        # Past to the next pixel value
        rgb += 1
        if rgb >= 3:
            # Past to the next pixel
            rgb = 0
            pixel += 1
        if pixel >= len(pixel_array[0]):
            # Past to the next pixel
            pixel = 0
            row += 1
    # convert hide message binary into intelligible string
    message_decoded = decode_message(hide_message[16 : 16 + message_length_bits])
    return print("MESSAGE: ", message_decoded)


encode(
    "Ici johann je suis la taupe!",
    "medium2.png",
)

# decode("SECRET.png")
