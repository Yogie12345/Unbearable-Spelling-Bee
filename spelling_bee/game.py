import pygame
import os
import random
from .words import WordBank

class SpellingBeeGame:
    def __init__(self, level):
        pygame.init()
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Spelling Bee - Grade " + str(level))

        self.level = level
        self.word_bank = WordBank(level)
        self.running = True
        self.current_word, self.current_description = self.word_bank.get_new_word()
        self.user_guess = "_" * len(self.current_word)

        # Initialize counters and state variables
        self.honey_jar_count = 0
        self.honey_bee_count = 0
        self.word_completed = False
        self.bee_count_message_visible = False
        self.jar_count_message_visible = False
        self.bee_count_message_timer = 0
        self.jar_count_message_timer = 0

        # Initialize feedback related variables
        self.feedback_message = ""  # Holds the feedback symbol ("✓" or "X")
        self.feedback_timer = 0  # Timer for how long the feedback is displayed
        self.feedback_duration = 240  # Duration to display feedback (in frames)

        # New duration for the jar count message visibility
        self.jar_count_message_duration = 120  # Example: show the "+1" message for 120 frames
        self.bee_count_message_duration = 120  # Duration for bee messages
        # Visibility control for the word bank
        self.word_bank_visible = True  # Initially set the word bank to be visible

        # Color definition for the word bank background
        self.word_bank_background_color = (200, 200, 200)  # Example color: light gray

        self.load_assets()  # Load images, fonts, etc.
        self.initialize_ui_elements()  # Setup UI elements such as buttons and boxes
        self.initialize_game()  # Setup game mechanics and initial state
        self.initialize_word_bank()  # Additional setup specific to the word bank panel if needed

    def load_assets(self):
        # Load images and fonts
        self.background_image = pygame.image.load(os.path.join('assets', 'images', 'background.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 28)
        self.more_honey_image = pygame.image.load('assets/images/harvesthoney.png').convert_alpha()
        self.go_to_maze_image = pygame.image.load('assets/images/tomazebutton.png').convert_alpha()

    def initialize_ui_elements(self):
        # Grid setup
        self.block_size = self.percent_of_width(4)  # Each block is 4% of screen width
        self.grid_cols = 12
        self.grid_rows = 6
        grid_width = self.block_size * self.grid_cols
        grid_height = self.block_size * self.grid_rows
        grid_start_x = (self.screen_width - grid_width) // 2 + 180
        grid_start_y = self.percent_of_height(20)
        self.grid_rect = pygame.Rect(grid_start_x, grid_start_y, grid_width, grid_height)

        # Description box below the grid
        self.desc_box_rect = pygame.Rect(
            grid_start_x,
            grid_start_y + grid_height + self.percent_of_height(2),
            grid_width,
            self.percent_of_height(10))

        # Guess box for displaying the current word being guessed
        self.guess_box_rect = pygame.Rect(
            self.desc_box_rect.left,
            self.desc_box_rect.bottom + self.percent_of_height(2),
            self.desc_box_rect.width,
            self.percent_of_height(10))

        # Word bank panel
        bank_width = self.percent_of_width(15)
        bank_height = self.percent_of_height(50)
        bank_start_x = self.grid_rect.x - bank_width - self.percent_of_width(2)
        bank_start_y = self.grid_rect.y
        self.word_bank_panel_rect = pygame.Rect(bank_start_x, bank_start_y, bank_width, bank_height)

        # Slider for toggling word bank visibility
        slider_x = self.word_bank_panel_rect.right - self.percent_of_width(3.5)
        slider_y = self.word_bank_panel_rect.y + self.percent_of_height(1)
        slider_width = self.percent_of_width(3)
        slider_height = self.percent_of_height(2)
        self.slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)

        # Buttons for game actions
        button_width = self.percent_of_width(10)
        button_height = self.percent_of_height(5)
        self.more_honey_button_rect = pygame.Rect(
            self.guess_box_rect.right + self.percent_of_width(2) - 1250,
            self.guess_box_rect.top - 350,
            button_width,
            button_height)
        self.go_to_maze_button_rect = pygame.Rect(
            self.more_honey_button_rect.x,
            self.more_honey_button_rect.bottom + self.percent_of_height(5),
            button_width,
            button_height)
        
    def initialize_game(self):
        # Setup initial game state or variables
        self.letter_bank = self.word_bank.create_letter_bank()  # assuming create_letter_bank is a method that setups letter bank
        self.randomized_letter_positions = self.random_letter_pos()  # Setup random positions for letters

    def initialize_word_bank(self):
        # Assuming the word bank is to the left of the letter grid
        bank_width = self.percent_of_width(15)  # Width as 15% of screen width, adjust as needed
        bank_height = self.percent_of_height(20)  # Height as 60% of screen height, adjust as needed
        
        bank_start_x = self.grid_rect.x - bank_width - self.percent_of_width(2)  # 2% padding from the grid
        bank_start_y = self.grid_rect.y  # Align top with the grid

        self.word_bank_panel_rect = pygame.Rect(bank_start_x, bank_start_y, bank_width, bank_height)
        self.word_bank_scroll_position = 0  # Start scroll position
        self.word_bank_scroll_step = 20  # Scroll step for mouse wheel or buttons

        # Define background color for the word bank area if not defined elsewhere
        self.word_bank_background_color = (212, 160, 23)

        # Define the height of each word with padding for the word bank
        self.word_height_with_padding = 40  # Example height, adjust based on your UI needs
        
    def percent_of_width(self, percent):
        return int((percent / 100) * self.screen_width)

    def percent_of_height(self, percent):
        return int((percent / 100) * self.screen_height)
    
    def display_word_bank(self):
        # Drawing the background for the word bank panel
        pygame.draw.rect(self.screen, self.word_bank_background_color, self.word_bank_panel_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.word_bank_panel_rect, 3)  # Border

        if self.word_bank_visible:
            # Start y position is taken from the top of the word bank panel rect
            start_y = self.word_bank_panel_rect.y + 10 - self.word_bank_scroll_position
            visible_words = self.word_bank.get_all_words()
            
            for word in visible_words:
                word_surface = self.font.render(word, True, (0, 0, 0))
                if start_y + self.word_height_with_padding <= self.word_bank_panel_rect.y + self.word_bank_panel_rect.height:
                    self.screen.blit(word_surface, (self.word_bank_panel_rect.x + 10, start_y))
                start_y += self.word_height_with_padding
                
                # Stop drawing if we've reached the end of the visible panel
                if start_y > self.word_bank_panel_rect.y + self.word_bank_panel_rect.height:
                    break
    
    def display_word_bank_instruction(self):
        if not self.word_bank_visible:
            instruction_text = "Click to open word bank!"
            instruction_font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 20)
            instruction_surface = instruction_font.render(instruction_text, True, (0, 0, 0))
            
            instruction_x = self.slider_rect.x - 127  # Positioning it to the left of the slider, adjust the value as needed
            instruction_y = self.slider_rect.centery
            instruction_rect = instruction_surface.get_rect(center=(instruction_x, instruction_y))
            
            bg_rect = instruction_rect.inflate(20, 10)  # Adjust padding as needed
            pygame.draw.rect(self.screen, (212, 160, 23), bg_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, 2)  # Black border
            
            self.screen.blit(instruction_surface, instruction_rect)

    def draw_slider(self):
        # Background of the slider
        pygame.draw.rect(self.screen, (180, 180, 180), self.slider_rect)
        # Slider button inside, color changes based on visibility state
        button_color = (0, 255, 0) if self.word_bank_visible else (255, 0, 0)
        pygame.draw.rect(self.screen, button_color, self.slider_rect.inflate(-10, -5))

    #Render the word description to the screen
    def display_word_description(self): 
        
        light_yellow = (255, 255, 254)
        red_color = (255, 0, 0)

        desc_font = pygame.font.Font(os.path.join('assets', 'fonts', 'OpenSans-Regular.ttf'), 24)

        desc_surface = desc_font.render(self.current_description, True, red_color)
        desc_rect = desc_surface.get_rect(center=(self.desc_box_rect.centerx, self.desc_box_rect.centery - 30))

        pygame.draw.rect(self.screen, light_yellow, self.desc_box_rect) 
        self.screen.blit(desc_surface, desc_rect)

    #Drawing the word guess box 
    def display_guess_box(self):
        pygame.draw.rect(self.screen, (212, 160, 23), self.guess_box_rect)  # Fill color
        pygame.draw.rect(self.screen, (255, 255, 255), self.guess_box_rect, self.percent_of_width(0.5))  # Border 

   #Shuffling the position of the letters seen on the grid 
    def random_letter_pos(self):
        # Create positions for each letter
        all_cell_positions = [(col, row) for col in range(self.grid_cols) for row in range(self.grid_rows)]
        random.shuffle(all_cell_positions)
        return {letter: all_cell_positions[i] for i, letter in enumerate(self.letter_bank)}

    #Displaying the letter grid 
    def display_letter_bank(self): 
        golden_yellow = (255, 223, 0)
        white_color = (0,0,0)

        #Fill the grid with yellow 
        pygame.draw.rect(self.screen, golden_yellow, self.grid_rect)

        total_cells = self.grid_cols * self.grid_rows
        #Generate a list of all cell positions 
        all_cell_positions = [(col, row) for col in range(self.grid_cols) for row in range(self.grid_rows)]
        random.shuffle(all_cell_positions) #Shuffle the list so we get random positions 


        # Drawing grid 
        for col in range(self.grid_cols):
            for row in range(self.grid_rows): 
                # Determine the position of the current cell
                cell_x = self.grid_rect.x + col * self.block_size
                cell_y = self.grid_rect.y + row * self.block_size
                cell_rect = pygame.Rect(cell_x, cell_y, self.block_size, self.block_size)
                
                #cell border
                pygame.draw.rect(self.screen, white_color, cell_rect, 1)
        
        #Placing the letters in the cells
        for letter, (col, row) in self.randomized_letter_positions.items(): 
            cell_x = self.grid_rect.x + col * self.block_size
            cell_y = self.grid_rect.y + row * self.block_size
            letter_surface = self.font.render(letter, True, white_color)
            letter_rect = letter_surface.get_rect(center=(cell_x + self.block_size / 2, cell_y + self.block_size / 2))
            self.screen.blit(letter_surface, letter_rect)
    
    #Displaying the word to be guessed 
    def display_guess(self): 
        underline_color = (0, 0, 0)  
        underline_length = 40 
        underline_spacing = 20 
        underline_thickness = 2


        # Starting positions for the first underline
        total_length = (len(self.current_word) - 1) * (underline_length + underline_spacing) + underline_length
        start_x = self.guess_box_rect.centerx - total_length // 2
        start_y = self.guess_box_rect.centery - 90

        for i, char in enumerate(self.current_word):
            # Calculate the position for each underline based on the index
            position_x = start_x + i * (underline_length + underline_spacing)
            underline_rect = pygame.Rect(position_x, start_y - underline_thickness // 2, underline_length, underline_thickness)
            pygame.draw.rect(self.screen, underline_color, underline_rect)

            # Display the correctly guessed letter above the underline
            if self.user_guess[i] != '_':
                letter_surface = self.font.render(self.user_guess[i], True, underline_color)
                letter_rect = letter_surface.get_rect(center=(position_x + underline_length // 2, start_y - 30))  # Adjust Y position as needed
                self.screen.blit(letter_surface, letter_rect)

    #Check if the complete word has been spelt 
    def check_word_completion(self):
        if "_" not in self.user_guess:
            self.word_completed = True
            self.honey_jar_count += 1  # Increment the honey jar count
            
            # Trigger the "+1" message for the honey jar
            self.jar_count_message_visible = True
            self.jar_count_message_timer = self.jar_count_message_duration
            
    #Displaying the buttons
    def display_buttons(self):
        self.screen.blit(self.more_honey_image, self.more_honey_button_rect.topleft)
        self.screen.blit(self.go_to_maze_image, self.go_to_maze_button_rect.topleft)

    #Displaying the counters 
    def display_counters(self):
        jar_msg = f"Number of Jars: {self.honey_jar_count}"
        bee_msg = f"Number of Bees: {self.honey_bee_count}"
        
        jar_surface = self.font.render(jar_msg, True, (0, 0, 0))
        bee_surface = self.font.render(bee_msg, True, (0, 0, 0))

        #Calculating width and postioning for counter boxes 
        space_between_counters = 20  
        total_counters_width = jar_surface.get_width() + bee_surface.get_width() + space_between_counters
        start_x = self.grid_rect.centerx - total_counters_width // 2
        counter_y = self.grid_rect.top - jar_surface.get_height()  

        # background boxes for counters
        jar_background_rect = pygame.Rect(start_x, counter_y, jar_surface.get_width() + 20, jar_surface.get_height() + 10)  
        bee_background_rect = pygame.Rect(start_x + jar_background_rect.width + space_between_counters, counter_y, bee_surface.get_width() + 20, bee_surface.get_height() + 10)

        pygame.draw.rect(self.screen, (212, 160, 23), jar_background_rect)  
        pygame.draw.rect(self.screen, (212, 160, 23), bee_background_rect)  

        pygame.draw.rect(self.screen, (255, 255, 255), jar_background_rect, 5) 
        pygame.draw.rect(self.screen, (255, 255, 255), bee_background_rect, 5) 

        self.screen.blit(jar_surface, (jar_background_rect.x + 10, jar_background_rect.y + 5))
        self.screen.blit(bee_surface, (bee_background_rect.x + 10, bee_background_rect.y + 5))
        
        # Display the "+1" message next to the number of bees, if applicable
        if self.bee_count_message_visible:
            plus_one_msg = "+1"
            plus_one_font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 24)
            plus_one_color = (255, 0, 0)  # Red color for the "+1" message
            
            plus_one_surface = plus_one_font.render(plus_one_msg, True, plus_one_color)
            plus_one_rect = plus_one_surface.get_rect(left=bee_background_rect.right + 10, centery=bee_background_rect.centery)

            self.screen.blit(plus_one_surface, plus_one_rect)
            self.bee_count_message_timer -= 1

            # Hide the message when the timer runs out
            if self.bee_count_message_timer <= 0:
                self.bee_count_message_visible = False
                
        if self.jar_count_message_visible:
            plus_one_jar_msg = "+1"
            plus_one_jar_font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 24)
            plus_one_jar_color = (0, 255, 0)  # Green color for the "+1" message
            
            plus_one_jar_surface = plus_one_jar_font.render(plus_one_jar_msg, True, plus_one_jar_color)
            plus_one_jar_rect = plus_one_jar_surface.get_rect(left=jar_background_rect.right, centery=jar_background_rect.centery)

            self.screen.blit(plus_one_jar_surface, plus_one_jar_rect)
            self.jar_count_message_timer -= 1

            # Hide the message when the timer runs out
            if self.jar_count_message_timer <= 0:
                self.jar_count_message_visible = False

    #Check if button was pressed for new word and grid 
    def on_mouse_button_down(self, mouse_pos):
        if self.word_completed:
            if self.more_honey_button_rect.collidepoint(mouse_pos):
                self.reset_game()
            elif self.go_to_maze_button_rect.collidepoint(mouse_pos):
                self.running = False

    #Check the mouse click that was made on the grid 
    def on_letter_selected(self, mouse_pos): 
        if self.grid_rect.collidepoint(mouse_pos):
            col = (mouse_pos[0] - self.grid_rect.x) // self.block_size
            row = (mouse_pos[1] - self.grid_rect.y) // self.block_size

            # Find the clicked cell's letter
            clicked_letter = None
            for letter, (l_col, l_row) in self.randomized_letter_positions.items():
                if l_col == col and l_row == row:
                    clicked_letter = letter
                    break  # Found the clicked letter, exit the loop

            # If a letter was clicked, process it
            if clicked_letter:
                self.process_letter_selection(clicked_letter)

                # Remove the letter from the dictionary if it exists
                if clicked_letter in self.randomized_letter_positions:
                    del self.randomized_letter_positions[clicked_letter]



    #Check if the user selected letter is in the word to be guessed 
    def process_letter_selection(self, letter):
        # Check if the letter is in the word
        guess_was_correct = letter in self.current_word

        if guess_was_correct:
            # Update all positions of the guessed letter in the current word
            indices = [pos for pos, char in enumerate(self.current_word) if char == letter]
            for index in indices:
                # Construct the new user_guess including the newly correctly guessed letter
                self.user_guess = self.user_guess[:index] + letter + self.user_guess[index + 1:]
            self.feedback_message = "✓"
        else:
            self.honey_bee_count += 1
            self.feedback_message = "X"
            self.bee_count_message_visible = True
            self.bee_count_message_timer = self.jar_count_message_duration  # Use the jar count duration for bees as well

        # Reset the feedback timer for both correct and incorrect guesses
        self.feedback_timer = self.feedback_duration

        # Always remove the letter from the grid and update the game state
        if letter in self.randomized_letter_positions:
            del self.randomized_letter_positions[letter]

        self.display_guess()
        self.check_word_completion()


    def display_feedback(self):
        if self.feedback_timer > 0:
            feedback_pos = (self.screen_width // 2, self.screen_height // 2)
            feedback_font = pygame.font.Font('assets/fonts/DejaVuSans.ttf', 96)
            feedback_color = (0, 255, 0) if self.feedback_message == "✓" else (255, 0, 0)

            feedback_surface = feedback_font.render(self.feedback_message, True, feedback_color)
            feedback_rect = feedback_surface.get_rect(center=feedback_pos)

            self.screen.blit(feedback_surface, feedback_rect)

            self.feedback_timer -= 1
            
    #Reset the game for a new word and grid 
    def reset_game(self):
        self.word_completed = False
        self.current_word, self.current_description = self.word_bank.get_new_word()
        self.user_guess = "_" * len(self.current_word)
        self.randomized_letter_positions = self.random_letter_pos()
            
    #Function that will run spelling bee game 
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos, event.button)

            self.update_screen()

    def handle_mouse_click(self, pos, button):
        if self.slider_rect.collidepoint(pos):
            # Toggle the visibility of the word bank
            self.word_bank_visible = not self.word_bank_visible
        elif self.word_bank_panel_rect.collidepoint(pos) and self.word_bank_visible:
            # Handle scrolling in the word bank
            if button == 4:  # Mouse wheel scroll up
                self.word_bank_scroll_position = max(self.word_bank_scroll_position - self.word_bank_scroll_step, 0)
            elif button == 5:  # Mouse wheel scroll down
                max_scroll = max(len(self.word_bank.get_all_words()) * self.word_height_with_padding - self.word_bank_panel_height, 0)
                self.word_bank_scroll_position = min(self.word_bank_scroll_position + self.word_bank_scroll_step, max_scroll)
        elif self.word_completed:
            self.on_mouse_button_down(pos)
        else:
            self.on_letter_selected(pos)

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))

        self.display_counters()
        self.display_letter_bank()
        self.display_word_description()
        self.display_guess()
        self.display_feedback()

        if self.word_bank_visible:
            self.display_word_bank()

        # Draw the slider for the word bank visibility toggle
        self.draw_slider()

        if not self.word_bank_visible:
            self.display_word_bank_instruction()

        if self.word_completed:
            self.display_buttons()

        pygame.display.flip()

