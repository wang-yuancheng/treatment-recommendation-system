from app import create_app

app = create_app()

if __name__ == "__main__":
   print("starting Flask server...")
   app.run(host='0.0.0.0', port=5555, debug=True)