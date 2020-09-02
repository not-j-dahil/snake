import tkinter as tk
from PIL import Image, ImageTk

MOVE_INCREMENT = 20

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = (200, 100)
        self.score = 0
        
        self.load_assets()
        self.create_objects()

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            
            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()
    
    def create_objects(self):
        self.create_text(
            45,12, text=f"Score {self.score}", tag="score", fill="#fff", font=("TkDefaultFont", 14)
        )
        for x_pos, y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag= "food")
        self.create_rectangle(7,27,593,613, outline="#999999")
    
    def move_snake(self):
        head_x_pos, head_y_pos = self.snake_positions[0]
        new_head_pos = (head_x_pos + MOVE_INCREMENT, head_y_pos)

        self.snake_positions = [new_head_pos] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)




root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake()
board.pack()

#start window
root.mainloop()