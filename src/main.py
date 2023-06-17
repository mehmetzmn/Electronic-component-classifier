import os
from flask import Flask, request, jsonify, render_template
from scrap import Scrap
from util import Util




def changeName(ROOT):
    PATH = os.path.join(ROOT, "data")
    for i, file in enumerate(os.listdir(PATH)):
        if file == ".DS_Store":
                continue
        for index, file2 in enumerate(sorted(os.listdir(os.path.join(PATH, file)))):
            if file2 == ".DS_Store":
                continue
            new_name = "image" + str(index + 1) + ".jpg"
            original_path = os.path.join(PATH, file, file2)
            new_path = os.path.join(PATH, file, new_name)
            os.rename(original_path, new_path)
            # os.rename(os.path.join(PATH, file, file2), os.path.join(PATH, file, str(index + 1)+".jpg"))




app = Flask(__name__, static_folder="UI")

@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    image_data = request.form['image_data']

    model = Util("/Users/user/Desktop/Python projects/image classification/models/my_model", 
                    "/Users/user/Desktop/Python projects/image classification/models/model_classes.json")

    response = jsonify(model.classify_image(image_data, None))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



def main():

    classes = ['resistor', 'capacitor', 'diode', 'transistor', 'integrated circuit']

    # scrap = Scrap('IC', "/Path/to/the/Browser/app", \
    #             "/Path/to/the/chromedriver/chromedriver", \
    #             "/Path/to/the/data", use_container_len=True)

    # scrap.fit()
    
    util_obj = Util("/Users/user/Desktop/Python projects/image classification/models/my_modelv2", 
                    "/Users/user/Desktop/Python projects/image classification/models/model_classes.json")
    test_img = util_obj.img_to_base64("/Users/user/Desktop/Python projects/image classification/test/test 9.jpeg")

    print(util_obj.classify_image(test_img, None))



if __name__ == "__main__":
    # main()
    # changeName("Path")
    app.run(port=5000)

