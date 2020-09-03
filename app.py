from random import randint
import tkinter as tk
from PIL import Image, ImageTk

MOVE_INCREMENT = 20
moves_per_second = 10
GAME_SPEED = 1000 // moves_per_second # // floor division

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)
        
        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions) #75 = 75 milliseconds | call function name NOT function call ('perform_actions()')

    def load_assets(self):
        '''Load images for snake and food from assets'''
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            
            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()
    
    def create_objects(self):
        '''Create objects with the loaded assets'''
        self.create_text(
            100,12, 
            text=f"Score {self.score} (speed: {moves_per_second})", 
            tag="score", 
            fill="#fff", 
            font=("TkDefaultFont", 14)
        )
        for x_pos, y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag= "food")
        self.create_rectangle(7,27,593,613, outline="#999999")
    
    def move_snake(self):
        head_x_pos, head_y_pos = self.snake_positions[0]

        if self.direction == "Left":
            new_head_pos = (head_x_pos - MOVE_INCREMENT, head_y_pos)
        elif self.direction == "Right":
            new_head_pos = (head_x_pos + MOVE_INCREMENT, head_y_pos)
        elif self.direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - MOVE_INCREMENT)
        elif self.direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + MOVE_INCREMENT)

        self.snake_positions = [new_head_pos] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        '''Recursive function - Refresh window 
        | Checks collisions
        | Moves snake'''
        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        '''Check snake collision to border or itself'''
        head_x_pos, head_y_pos = self.snake_positions[0]

        return (
            head_x_pos in (0,600)
            or head_y_pos in (20, 620)
            or (head_x_pos, head_y_pos) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        '''keybindings and direction change'''
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites #prevent eating itself 
        ):
            self.direction = new_direction
    
    def check_food_collision(self):
        '''Checks if food eaten -> Move food randomly'''
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(
                score, 
                text=f"Score: {self.score} (speed: {moves_per_second})", 
                tag="score"
            )

    def set_new_food_position(self):
        while True:
            x_pos = randint(1, 29) * MOVE_INCREMENT
            y_pos = randint(3, 30) * MOVE_INCREMENT
            food_pos = (x_pos, y_pos)

            if food_pos not in self.snake_positions:
                return food_pos

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )



root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake()
board.pack()

#start window
root.mainloop()
