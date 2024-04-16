from flask import Flask,request,render_template
import google.generativeai as palm
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_CtbcXs9Mk9uxXX8yvWuOnWiLJQ9zHFW1Kcbjf"
palm.configure(api_key="AIzaSyATy8F6EfovHdxIN83uA09dKmeyHVHSZt4")
model = {
    "model": "models/chat-bison-001",
}

name = ""
flag=1

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    global name,flag
    if flag == 1:
        name = request.form.get("q")
        flag=0
    return(render_template("main.html",r=name))

@app.route("/text",methods=["GET","POST"])
def text():
    return(render_template("text.html")) 

@app.route("/text_generator",methods=["GET","POST"])
def text_generator():
    q = request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_generator.html",r=r.last)) 

@app.route("/image",methods=["GET","POST"])
def image():
    return(render_template("image.html")) 

@app.route("/image_generator",methods=["GET","POST"])
def image_generator():
    q = request.form.get("q")
    r = replicate.run(
        "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
        input = {
            "prompt" : q
        }
    )
    return(render_template("image_generator.html",r=r[0])) 

@app.route("/music",methods=["GET","POST"])
def music():
    return(render_template("music.html")) 

@app.route("/music_generator",methods=["GET","POST"])
def music_generator():
    q = request.form.get("q")
    r = replicate.run(
        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
        input = {
            "prompt" : q,
            "duration" : 5
        }
    )
    return(render_template("music_generator.html",r=r)) 

@app.route("/video",methods=["GET","POST"])
def video():
    return(render_template("video.html")) 

@app.route("/video_generator",methods=["GET","POST"])
def video_generator():
    q = request.form.get("q")
    r = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input = {
            "prompt" : q,
            "num_frames" : 5
        }
    )
    return(render_template("video_generator.html",r=r[0])) 

@app.route("/end",methods=["GET","POST"])
def end():
    global flag
    print("ending process.....")
    flag = 1
    return(render_template("index.html"))    
    
if __name__ == "__main__":
    app.run()
