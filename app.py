from flask import Flask, render_template, request, flash, url_for, redirect, session
import pickle
import numpy as np
import sqlite3
import random
from PIL import Image

model = pickle.load(open("clf.pkl","rb"))
app = Flask(__name__)
app.secret_key = 'e4d4f013f0eb16f4b0ed5adb998d27aa'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index', methods=['GET'])
def index():
    if 'username' in session:
        # If the user is logged in, display a welcome message with their name
        return render_template('index.html', username=session['username'])
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if the user exists in the database
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user:
            # If the user exists, check their password
            if password == user[2]:
                # If the password is correct, store the user's name in a session variable
                session['username'] = user[1]
                conn.close()
                return redirect(url_for('index'))
            else:
                # If the password is incorrect, show a message popup and render the login page again
                flash('Invalid username or password.', 'error')
                conn.close()
                return render_template('login.html')
        else:
            # If the user does not exist, insert their credentials into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            # Show a message popup and render the success page
            flash('User created successfully. You can now log in with your credentials.', 'success')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():

    lang_vocab = request.form['lang_vocab']
    memory = request.form['memory']
    speed = request.form['speed']
    visual = request.form['visual']
    audio = request.form['audio']
    survey = request.form['survey']

    array = np.array([[lang_vocab, memory, speed, visual, audio, survey]])

    label = int(model.predict(array))
    #Giving final output to user depending upon the model prediction.
    if(label == 0):
        return render_template('result1.html')
        # output = "There is a high chance of the applicant to have dyslexia."
    elif(label == 1):
        return render_template('result2.html')
        # output = "There is a moderate chance of the applicant to have dyslexia."
    else:
        return render_template('result3.html')

    # Return the prediction to the user
    return render_template('predict.html')


@app.route('/audio',methods=['GET'])
def audio():
    return render_template('audio.html')

@app.route('/story',methods=['GET'])
def story():
    return render_template('story.html')

@app.route('/test', methods=['GET'])
def test():
    return render_template('predict.html')

@app.route('/level_one',methods=['GET'])
def level_one():
    return render_template('level1.html')

@app.route('/level_two',methods=['GET'])
def level_two():
    return render_template('level2.html')

@app.route('/level_three', methods=['GET'])
def level_three():
    return render_template('level3.html')



# List of possible images and their corresponding words
images = [
    {'image': './static/images/game_img/apple.jpg', 'word': 'apple'},
    {'image': './static/images/game_img/balloons.jpg', 'word': 'balloons'},
    {'image': './static/images/game_img/banana.jpg', 'word': 'banana'},
    {'image': './static/images/game_img/buffalo.jpg', 'word': 'buffalo'},
    {'image': './static/images/game_img/butterfly.jpg', 'word': 'butterfly'},
    {'image': './static/images/game_img/carrot.jpg', 'word': 'carrot'},
    {'image': './static/images/game_img/cat.jpg', 'word': 'cat'},
    {'image': './static/images/game_img/chair.jpg', 'word': 'chair'},
    {'image': './static/images/game_img/cherry.jpg', 'word': 'cherry'},
    {'image': './static/images/game_img/chess.jpg', 'word': 'chess'},
    {'image': './static/images/game_img/corn.jpg', 'word': 'corn'},
    {'image': './static/images/game_img/cow.jpg', 'word': 'cow'},
    {'image': './static/images/game_img/crow.jpg', 'word': 'crow'},
    {'image': './static/images/game_img/daisy.jpg', 'word': 'daisy'},
    {'image': './static/images/game_img/deer.jpg', 'word': 'deer'},
    {'image': './static/images/game_img/dog.jpg', 'word': 'dog'},
    {'image': './static/images/game_img/dolphin.jpg', 'word': 'dolphin'},
    {'image': './static/images/game_img/duck.jpg', 'word': 'duck'},
    {'image': './static/images/game_img/elephant.jpg', 'word': 'elephant'},
    {'image': './static/images/game_img/giraffe.jpg', 'word': 'giraffe'},
    {'image': './static/images/game_img/grapes.jpg', 'word': 'grapes'},
    {'image': './static/images/game_img/hen.jpg', 'word': 'hen'},
    {'image': './static/images/game_img/horse.jpg', 'word': 'horse'},
    {'image': './static/images/game_img/lion.jpg', 'word': 'lion'},
    {'image': './static/images/game_img/lotus.jpg', 'word': 'lotus'},
    {'image': './static/images/game_img/monkey.jpg', 'word': 'monkey'},
    {'image': './static/images/game_img/onion.jpg', 'word': 'onion'},
    {'image': './static/images/game_img/orange.jpg', 'word': 'orange'},
    {'image': './static/images/game_img/ostrich.jpg', 'word': 'ostrich'},
    {'image': './static/images/game_img/panda.jpg', 'word': 'panda'},
    {'image': './static/images/game_img/parrot.jpg', 'word': 'parrot'},
    {'image': './static/images/game_img/peacock.jpg', 'word': 'peacock'},
    {'image': './static/images/game_img/piegon.jpg', 'word': 'piegon'},
    {'image': './static/images/game_img/pineapple.jpg', 'word': 'pineapple'},
    {'image': './static/images/game_img/potato.jpg', 'word': 'potato'},
    {'image': './static/images/game_img/pumpkin.jpg', 'word': 'pumpkin'},
    {'image': './static/images/game_img/rabbit.jpg', 'word': 'rabbit'},
    {'image': './static/images/game_img/rose.jpg', 'word': 'rose'},
    {'image': './static/images/game_img/shark.jpg', 'word': 'shark'},
    {'image': './static/images/game_img/sheep.jpg', 'word': 'sheep'},
    {'image': './static/images/game_img/sparrow.jpg', 'word': 'sparrow'},
    {'image': './static/images/game_img/strawberry.jpg', 'word': 'strawberry'},
    {'image': './static/images/game_img/sunflower.jpg', 'word': 'sunflower'},
    {'image': './static/images/game_img/table.jpg', 'word': 'table'},
    {'image': './static/images/game_img/tiger.jpg', 'word': 'tiger'},
    {'image': './static/images/game_img/tomato.jpg', 'word': 'tomato'},
    {'image': './static/images/game_img/tortoise.jpg', 'word': 'tortoise'},
    {'image': './static/images/game_img/watermelon.jpg', 'word': 'watermelon'},
    {'image': './static/images/game_img/whale.jpg', 'word': 'whale'},
    {'image': './static/images/game_img/zebra.jpg', 'word': 'zebra'}

]

@app.route('/shuffle',methods=['GET','POST'])
def shuffle():
    global images
    if not images:
        images = [
            {'image': './static/images/game_img/apple.jpg', 'word': 'apple'},
    {'image': './static/images/game_img/balloons.jpg', 'word': 'balloons'},
    {'image': './static/images/game_img/banana.jpg', 'word': 'banana'},
    {'image': './static/images/game_img/buffalo.jpg', 'word': 'buffalo'},
    {'image': './static/images/game_img/butterfly.jpg', 'word': 'butterfly'},
    {'image': './static/images/game_img/carrot.jpg', 'word': 'carrot'},
    {'image': './static/images/game_img/cat.jpg', 'word': 'cat'},
    {'image': './static/images/game_img/chair.jpg', 'word': 'chair'},
    {'image': './static/images/game_img/cherry.jpg', 'word': 'cherry'},
    {'image': './static/images/game_img/chess.jpg', 'word': 'chess'},
    {'image': './static/images/game_img/corn.jpg', 'word': 'corn'},
    {'image': './static/images/game_img/cow.jpg', 'word': 'cow'},
    {'image': './static/images/game_img/crow.jpg', 'word': 'crow'},
    {'image': './static/images/game_img/daisy.jpg', 'word': 'daisy'},
    {'image': './static/images/game_img/deer.jpg', 'word': 'deer'},
    {'image': './static/images/game_img/dog.jpg', 'word': 'dog'},
    {'image': './static/images/game_img/dolphin.jpg', 'word': 'dolphin'},
    {'image': './static/images/game_img/duck.jpg', 'word': 'duck'},
    {'image': './static/images/game_img/elephant.jpg', 'word': 'elephant'},
    {'image': './static/images/game_img/giraffe.jpg', 'word': 'giraffe'},
    {'image': './static/images/game_img/grapes.jpg', 'word': 'grapes'},
    {'image': './static/images/game_img/hen.jpg', 'word': 'hen'},
    {'image': './static/images/game_img/horse.jpg', 'word': 'horse'},
    {'image': './static/images/game_img/lion.jpg', 'word': 'lion'},
    {'image': './static/images/game_img/lotus.jpg', 'word': 'lotus'},
    {'image': './static/images/game_img/monkey.jpg', 'word': 'monkey'},
    {'image': './static/images/game_img/onion.jpg', 'word': 'onion'},
    {'image': './static/images/game_img/orange.jpg', 'word': 'orange'},
    {'image': './static/images/game_img/ostrich.jpg', 'word': 'ostrich'},
    {'image': './static/images/game_img/panda.jpg', 'word': 'panda'},
    {'image': './static/images/game_img/parrot.jpg', 'word': 'parrot'},
    {'image': './static/images/game_img/peacock.jpg', 'word': 'peacock'},
    {'image': './static/images/game_img/piegon.jpg', 'word': 'piegon'},
    {'image': './static/images/game_img/pineapple.jpg', 'word': 'pineapple'},
    {'image': './static/images/game_img/potato.jpg', 'word': 'potato'},
    {'image': './static/images/game_img/pumpkin.jpg', 'word': 'pumpkin'},
    {'image': './static/images/game_img/rabbit.jpg', 'word': 'rabbit'},
    {'image': './static/images/game_img/rose.jpg', 'word': 'rose'},
    {'image': './static/images/game_img/shark.jpg', 'word': 'shark'},
    {'image': './static/images/game_img/sheep.jpg', 'word': 'sheep'},
    {'image': './static/images/game_img/sparrow.jpg', 'word': 'sparrow'},
    {'image': './static/images/game_img/strawberry.jpg', 'word': 'strawberry'},
    {'image': './static/images/game_img/sunflower.jpg', 'word': 'sunflower'},
    {'image': './static/images/game_img/table.jpg', 'word': 'table'},
    {'image': './static/images/game_img/tiger.jpg', 'word': 'tiger'},
    {'image': './static/images/game_img/tomato.jpg', 'word': 'tomato'},
    {'image': './static/images/game_img/tortoise.jpg', 'word': 'tortoise'},
    {'image': './static/images/game_img/watermelon.jpg', 'word': 'watermelon'},
    {'image': './static/images/game_img/whale.jpg', 'word': 'whale'},
    {'image': './static/images/game_img/zebra.jpg', 'word': 'zebra'}

    ]

    # Choose a random image and its corresponding word
    chosen_image = random.choice(images)
    word = chosen_image['word']

    # Remove the chosen image from the list to prevent repetition
    images.remove(chosen_image)

    # Open the image and resize it
    with Image.open(chosen_image['image']) as img:
        img = img.resize((300, 300))

        # Save the resized image to a temporary file
        temp_img_path = './static/images/temp.jpg'
        img.save(temp_img_path)

    # Shuffle the word
    shuffled_word = ''.join(random.sample(word, len(word)))

    # Render the template with the image and shuffled word
    return render_template('shuffle.html', image='./static/images/temp.jpg' + '?v=' + str(random.random()), shuffled_word=shuffled_word, word=word)


@app.route('/check_word', methods=['POST'])
def check_word():
    # Retrieve the original word and shuffled word from the form submission
    word = request.form['word']
    shuffled_word = request.form['shuffled_word']

    # Get the user's guess and check if it matches the original word
    guess = request.form['guess']
    if guess.lower() == word.lower():
        result = 'Correct 🎉 You Won The Game🎊'
    else:
        result = "Incorrect 🥹 Let's Practice more 😜"

    # Render the template with the result and the original image and word
    return render_template('result.html', result=result, image=request.form['image'], word=word)


@app.route('/play_again')
def play_again():
    # Redirect to the index route to start a new game
    return redirect(url_for('shuffle'))



if __name__ == '__main__':
    app.run(debug=True)

