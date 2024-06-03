import cv2
import pandas as pd

# Path to your image file
img_path = r'C:\Users\User\Downloads\Color-Detection-OpenCV-main\Color-Detection-OpenCV-main\colorpic.jpg'
img = cv2.imread(img_path)

# Declare global variables (to be used later)
clicked = False
r = g = b = x_pos = y_pos = 0

# Read the CSV file with pandas and give names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(r'C:\Users\User\Downloads\Color-Detection-OpenCV-main\Color-Detection-OpenCV-main\colors.csv',
                  names=index, header=None)


# Function to calculate the minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    if clicked:
        # Draw a rectangle with the color and display color name and RGB values
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
