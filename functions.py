from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import binascii
import base64
import os
import speech_recognition as sr
import pyttsx3


# Initialize recognizer object
r = sr.Recognizer()


def save_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def dalleUrl(prompt):
    import openai
    # openai.api_key = "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"
    openai.api_key = "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"

    # print(openai.api_key)

    res = openai.Image.create(
        prompt=""+prompt+"",
        n=1,
        size="1024x1024"
    )
    res = res["data"][0]["url"]

    return res



import openai 

def chatgpt(question):
    # openai.api_key = "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"
    openai.api_key = "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"

    model_engine = "text-davinci-003"
    prompt = "" + question + ""

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = completion.choices[0].text
    return response

def basicFormatAdded(addedTxt):
    return '<!DOCTYPE html><html><head>	<title style="font-family: "Orbitron", sans-serif; font-size: 48px; color: #00ff00; text-shadow: 2px 2px 4px #000000;">Text to Image Converter</title></head><body style="text-align:center;">	<h1>Text to Image Converter</h1>	<form action="/" method="post">		<label for="text">Enter your text to make image:</label><br>		<input type="text" id="text" name="text">		<br>		<button type="submit" name="submit">Convert to Image</button>	</form>    <form action="/question_answer" method="post">    <label for="text-2">ask any question:</label><br>    <input type="text" id="text-2" name="text"><br>    <button type="submit" name="submit">ask</button></form><form action="/all_pictures" method="get">  <button type="submit"        background-color: #4CAF50;border: none;color: white;padding: 10px 20px;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;cursor: pointer;border-radius: 5px;>View All Pictures</button></form>'+addedTxt+'</body></html>'

def basicFormat():
    return basicFormatAdded('')

def formatImage(image_url1):
    return basicFormatAdded('<img src="'+image_url1+'" alt="Image Description">')

def formatQuestion(question1):
    return basicFormatAdded('<h1>'+question1+'</h1>')
    
def append_to_last_line(file_path, string_to_append):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        last_line = lines[-1].strip() if lines else ''
        file.seek(0)
        file.truncate()
        file.write(''.join(lines[:-1]))
        file.write(last_line + string_to_append)

def append_to_image_url(string):
    string += '\n'
    print(string)
    def add_to_empty_line(file_path, text):
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip() == '':
                    lines[i] = text + '\n'
                    file.seek(0)
                    file.writelines(lines)
                    return
            lines.append(text + '\n')
            file.seek(0)
            file.writelines(lines)
    add_to_empty_line('imageUrl.txt', string)

def append_to_images(string):
    append_to_last_line('/images.txt', string)


def hex_to_html(hex_data):
    try:
        bytes.fromhex(hex_data)
    except ValueError:
        # The input string is not a valid hexadecimal string
        return None
    else:
        encoded_data = base64.b64encode(bytes.fromhex(hex_data)).decode('utf-8')
        return '<img src="data:image/jpeg;base64,{0}" alt="Example Image">'.format(encoded_data)
    

def save_image_as_rgba(url):
    # Download the image data
    response = requests.get(url)
    # Create a new image from the downloaded data
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    # Get the filename from the URL
    filename = os.path.basename(url)
    # Change the file extension to ".png"
    filename = os.path.splitext(filename)[0] + ".png"
    # Create a directory called "images" in the root directory
    directory = os.path.join(os.getcwd(), "images")
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save the image as a PNG file in the "images" directory
    filepath = os.path.join(directory, filename)
    image.save(filepath, "PNG")

def save_image_url_txt():
    return ''


def list_files_in_directory(directory):
    """
    Returns a list of file names in the given directory.
    """
    html423 = ''
    fileList = os.listdir(directory)
    for i in fileList:
        print('this is the file')
        print(i)
        html423 += '<img src="'
        html423 += i
        html423 += '">'
    return html423

def list_files_in_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines    


import requests

def check_image_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # raise an exception for 4xx/5xx status codes
        content_type = response.headers.get('content-type')
        if content_type.startswith('image/'):
            return True
        else:
            return False
    except (requests.exceptions.RequestException, AttributeError):
        return False

def formated_files_into_img_elements_from_txt_file(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    fileList = lines
    html123 = '    <style>.container {display: grid;grid-template-columns: repeat(5, 1fr);grid-gap: 10px;}img {width: 100%;height: auto;}</style><div class="container">'
    for i in reversed(fileList):
        if check_image_url(i):
            print('this is the file')
            print(i)
            html123 += '<img src="'
            html123 += i
            html123 += '">'
    html123 += '</div>'
    return html123    

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



