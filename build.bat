echo "Downloading dependencies..."
pip install -r requirements.txt
echo "Building..."
python build.py
echo "Done! You can find the app on your desktop."