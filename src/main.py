import os
from flask import Flask, request, jsonify, render_template
from scrap import Scrap
from util import Util




def changeName(ROOT):
    """
    Change the name of the images in the data folder.

    Parameters
    ----------
    ROOT : str
        Path to the root directory.

    Returns
    -------
    None

    """
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
    """
    Classify the image sent from the UI.

    Parameters
    ----------
    None

    Returns
    -------
    response : json
    """
    image_data = request.form['image_data']

    model = Util("path/to/models/my_modelv2", 
                    "path/to/models/model_classes.json")

    response = jsonify(model.classify_image(image_data, None))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



def main():

    classes = ['resistor', 'capacitor', 'diode', 'transistor', 'integrated circuit']

    # create a Scrap object
    # scrap = Scrap('IC', "/Path/to/the/Browser/app", \
    #             "/Path/to/the/chromedriver/chromedriver", \
    #             "/Path/to/the/data", use_container_len=True)

    # run the scrap
    # scrap.fit()
    

    # This part for testing the model
    # create a util object, loading the model and the classes from the json file
    util_obj = Util("path/to/models/my_modelv2", 
                    "path/to/models/model_classes.json")
    
    # turn images into base64 and classify it
    test_img = util_obj.img_to_base64("path/to/test/test 9.jpeg")

    # print the result
    print(util_obj.classify_image(test_img, None))



if __name__ == "__main__":
    # main()
    # changeName("Path")
    app.run(port=5000)

