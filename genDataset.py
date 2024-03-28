DATA_TYPE=["startBlock","waitXSecondBlock","userNameVar","showBlock","hideBlock"]
crosshair_size = 50


import tkinter as tk
from PIL import Image
import os, json
imgs = os.listdir('data')

dataset = []
def genDataset(img, data):
    out = {
        "imagefilename": img,
        "annotation": [
        ]
    }
    for i in data:
        out["annotation"].append({
            "label": i[0],
            "coordinates": {
                "x": i[1],
                "y": i[2],
                "width": (i[3]-i[1]),
                "height": (i[4]-i[2])
            }
        })
    return out

for image in imgs:
    if image == '.DS_Store':
        continue
    if image.endswith('.png') == False:
        continue
    data = []
    root = tk.Tk()
    # set tk to image size
    im = Image.open('data/'+image)
    width, height = im.size
    root.title(image)
    # create a canvas to draw on
    canvas = tk.Canvas(root, width=width, height=height,cursor="tcross")
    canvas.pack()
    # load an image and display it on the canvas
    img = tk.PhotoImage(file='data/'+image)
    canvas.create_image(width//2, height//2, image=img)
    # let user draw a rectangle
    rect_id = None

    def on_click(event):
        global start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

    def on_drag(event):
        global start_x, start_y, rect_id
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)
        move_crosshair(event)

    def on_release(event):
        global start_x, start_y, rect_id
        end_x, end_y = event.x, event.y
        canvas.coords(rect_id, start_x, start_y, end_x, end_y)
        root.update()
        # create a popup with a dropdown menu to select the label/add a new label
        popup = tk.Toplevel(root)
        popup.title('Label')
        label = tk.StringVar()
        label.set('Select a label')
        menu = tk.OptionMenu(popup, label, *DATA_TYPE)
        menu.pack()
        # create a button to submit the label

        def submit():
            global width, height
            print(label.get(), start_x, start_y, end_x, end_y)
            data.append([label.get(), start_x, start_y, end_x, end_y])
            # Create a red rectangle as the text background
            i=canvas.create_text(start_x+1, start_y - 16, text=label.get(), fill='white', anchor='nw')
            r=canvas.create_rectangle(canvas.bbox(i),fill="red",outline="red")
            canvas.tag_lower(r,i)
            # Destroy the popup
            popup.destroy()
        # add a button to submit the label
        # when a label is selected, add event to run submit
        popup.bind('<FocusOut>', lambda e: submit())
        
    canvas.bind('<Button-1>', on_click)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)
    # bind command z to undo
    def undo(event):
        if data:
            canvas.delete(data.pop())
        if rect_id:
            canvas.delete(rect_id)
    root.bind('<Command-z>', undo)
    root.bind('<Control-z>', undo)
    # add a close button

    def close():
        dataset.append(genDataset(image, data))
        root.destroy()
    button = tk.Button(root, text='Close', command=close)
    button.pack()
    crosshair = canvas.create_line(0, 0, crosshair_size, 0, fill='black',width=1)
    crosshair2 = canvas.create_line(0, 0, 0, crosshair_size, fill='black',width=1)

    def move_crosshair(event):
        canvas.coords(crosshair, event.x - crosshair_size, event.y, event.x + crosshair_size, event.y)
        canvas.coords(crosshair2, event.x, event.y - crosshair_size, event.x, event.y + crosshair_size)

    canvas.bind('<Motion>', move_crosshair)
    root.mainloop()



print(dataset)
with open('dataset.json', 'w') as f:
    json.dump(dataset, f)