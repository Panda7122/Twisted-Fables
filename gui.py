import tkinter
import game
from PIL import Image, ImageTk
screen_width = 1280
screen_height = 720
openGraveyard = 0
def buildScreen(width, height):
    global screen_height, screen_width
    root = tkinter.Tk()
    # root.geometry(f"{width}x{height}")
    screen_width = width
    screen_height = height
    root.resizable(False, False)
    # Place the window at the left edge of the screen
    root.update_idletasks()
    screen_h = root.winfo_screenheight()
    x = 0
    y = (screen_h - screen_height) // 2 if screen_h > screen_height else 0
    root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
    root.title("Twisted Fables")
    return root
def cleanScreen(root):
    for widget in root.winfo_children():
        widget.destroy()
def updateScreen(root:tkinter.Tk, g:game.game):
    if(g.canUpdate != 0):
        fieldSize = int(screen_width//21.3)
        if not hasattr(root, "canvas"):
            root.canvas = tkinter.Canvas(root, width=screen_width, height=screen_height, bg="#8F8F8F")
            root.canvas.grid(row=0, column=0, columnspan=9)
            pil_img = Image.open("./picture/fieldPiece.png")
            factor = fieldSize/pil_img.width
            pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
            root.field_piece_image = ImageTk.PhotoImage(pil_img)
            root.player_images = [None, None]
            for idx, player in enumerate(g.players[:2]):
                imgpath = player.identity.picture_awakend if (player.identity.idx == 2 and player.identity.AWAKEN == 1) else player.identity.picture
                pil_img = Image.open(imgpath)
                factor = fieldSize/pil_img.width
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                player_image = ImageTk.PhotoImage(pil_img)
                # Store reference to avoid garbage collection
                root.player_images[idx] = player_image
            root.buycard_image = [[None,None,None],[None,None,None],[None,None,None],[None]]
            width = 0.1 * screen_width / 3
            for i in range(4):
                for j in range(3 if i < 3 else 1):
                    imgpath = f'./picture/cards/{i*3+j+1}.png'
                    pil_img = Image.open(imgpath)
                    factor = width/pil_img.width
                    pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                    bc_img = ImageTk.PhotoImage(pil_img)
                    root.buycard_image[i][j] = bc_img
            pil_img = Image.open('./picture/heart.png')
            factor = 100/pil_img.height
            root.life_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/defense.png')
            factor = 100/pil_img.height
            root.defense_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/energy.png')
            factor = 100/pil_img.height
            root.energy_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            
            pil_img = Image.open('./picture/tokens/Awakening.png')
            factor = 100/pil_img.height
            root.awakenTK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/tokens/combo.png')
            factor = 100/pil_img.height
            root.comboTK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/tokens/QI.png')
            factor = 100/pil_img.height
            root.QITK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/tokens/tentacle.png')
            factor = fieldSize/pil_img.width
            root.tentacleTK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            width = 0.1 * screen_width / 3 / 3
            factor = width/pil_img.width
            pil_img = Image.open('./picture/tokens/blue_fate.png')
            root.bluefateTK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = Image.open('./picture/tokens/red_fate.png')
            root.redfateTK_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            
            pil_img = Image.open('./picture/card_back.png')
            factor =  1/6 * screen_height / pil_img.height
            root.deck_img = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
            pil_img = pil_img.rotate(180)
            root.deck_img_rotated = ImageTk.PhotoImage(pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS))
        canvas = root.canvas
        canvas.delete("all")
        # Draw field pieces
        for i in range(1,10):
            canvas.create_image(10 + i*fieldSize, screen_height//2 + 0.005*screen_height, image=root.field_piece_image, anchor="nw")
        # Draw players
        for idx, player in enumerate(g.players[:2]):
            canvas.create_image(10 + player.locate*fieldSize+(fieldSize//2), screen_height//2 + 0.005*screen_height, image=root.player_images[idx], anchor="s")
        # draw first player's hand
        hands_cards = [[],[]]
        total_area = 0.7 * screen_width
        for i in range(2):
            for card in g.players[i].hand:
                if(card <= 0):
                    continue
                imgpath = f'./picture/cards/{card}.png'
                pil_img = Image.open(imgpath)
                factor = (total_area / len(g.players[i].hand))/pil_img.width
                if (factor*pil_img.height) > 1/6 * screen_height:
                    factor = 1/6 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                if i == 1:
                    pil_img = pil_img.rotate(180)
                card_img = ImageTk.PhotoImage(pil_img)
                hands_cards[i].append(card_img)
        root.hands_cards = hands_cards
        
        
        for i in range(len(g.players[0].hand)):
            try:
                width = int(root.hands_cards[0][0].width())
                canvas.create_image(i*width, screen_height-100, image=root.hands_cards[0][i], anchor="sw")
            except:
                pass
        for i in range(len(g.players[1].hand)):
            width = int(root.hands_cards[1][0].width())
            try:
                canvas.create_image(i*width, 100, image=root.hands_cards[1][i], anchor="nw")
            except:
                pass
        # draw buy area
        width = 0.1 * screen_width / 3
        for i in range(4):
            for j in range(3 if i < 3 else 1):
                x = 0.87*screen_width + j*width
                y = 0.3*screen_height + i*(0.3*screen_height/4)
                try:
                    canvas.create_image(x, y, image=root.buycard_image[i][j], anchor="nw")
                    canvas.create_text(x + 0.5 * width, y+0.001*screen_height + (0.3*screen_height/16), text=f"{len(g.basicBuyDeck[i*3+j])}", anchor="center", fill="red", font=("Times New Roman", 16))
                except:
                    pass
        # draw buy skill
        skill_img = [[None,None,None],[None,None,None]]
        total_area = 0.7 * screen_width
        for i in range(2):
            if len(g.players[i].attackSkill):
                if(g.players[i].attackSkill[0] <= 0):
                    continue
                img_path = f'./picture/cards/{g.players[i].attackSkill[0]}.png'
                pil_img = Image.open(img_path)
                factor = 1/8 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                skill_img[i][0] = ImageTk.PhotoImage(pil_img)
            if len(g.players[i].defenseSkill):
                if(g.players[i].defenseSkill[0] <= 0):
                    continue
                img_path = f'./picture/cards/{g.players[i].defenseSkill[0]}.png'
                pil_img = Image.open(img_path)
                factor = 1/8 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                skill_img[i][1] = ImageTk.PhotoImage(pil_img)
            if len(g.players[i].moveSkill):
                if(g.players[i].moveSkill[0] <= 0):
                    continue
                img_path = f'./picture/cards/{g.players[i].moveSkill[0]}.png'
                pil_img = Image.open(img_path)
                factor = 1/8 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                skill_img[i][2] = ImageTk.PhotoImage(pil_img)
        root.skill_img =skill_img
        for i in range(3):
            if root.skill_img[0][i] is None:
                continue
            canvas.create_image(0.7*screen_width + i*root.skill_img[0][i].width(), screen_height-100-root.deck_img.height(), image=root.skill_img[0][i], anchor="sw")
        for i in range(3):
            if root.skill_img[1][i] is None:
                continue
            canvas.create_image(0.7*screen_width + i*root.skill_img[1][i].width(), 100+root.deck_img.height(), image=root.skill_img[1][i], anchor="nw")
        # draw life, sheild, energy
        canvas.create_image(0, screen_height-100, image = root.life_img, anchor = "nw")
        canvas.create_text(150, screen_height-100, text=f"{g.players[0].identity.life:2}/{g.players[0].identity.maxlife}", anchor="nw", fill="black", font=("Times New Roman", 32))
        canvas.create_image(0, 0, image = root.life_img, anchor = "nw")
        canvas.create_text(150, 0, text=f"{g.players[1].identity.life:2}/{g.players[1].identity.maxlife}", anchor="nw", fill="black", font=("Times New Roman", 32))
        
        canvas.create_image(300, screen_height-100, image = root.defense_img, anchor = "nw")
        canvas.create_text(400, screen_height-100, text=f"{g.players[0].identity.defense}/{g.players[0].identity.maxdefense}", anchor="nw", fill="black", font=("Times New Roman", 32))
        canvas.create_image(300, 0, image = root.defense_img, anchor = "nw")
        canvas.create_text(400, 0, text=f"{g.players[1].identity.defense}/{g.players[1].identity.maxdefense}", anchor="nw", fill="black", font=("Times New Roman", 32))
        
        canvas.create_image(500, screen_height-100, image = root.energy_img, anchor = "nw")
        canvas.create_text(650, screen_height-100, text=f"{g.players[0].identity.energy}/25", anchor="nw", fill="black", font=("Times New Roman", 32))
        canvas.create_image(500, 0, image = root.energy_img, anchor = "nw")
        canvas.create_text(650, 0, text=f"{g.players[1].identity.energy}/25", anchor="nw", fill="black", font=("Times New Roman", 32))
        
        #deck
        canvas.create_image(0.7*screen_width, screen_height-100, image=root.deck_img, anchor = "sw")
        canvas.create_text(0.7*screen_width + root.deck_img.width()//2, screen_height-100,text=f"{len(g.players[0].deck)}", anchor="s", fill="white", font=("Times New Roman", 32, "bold"))
        
        
        canvas.create_image(0.7*screen_width, 100, image=root.deck_img_rotated, anchor = "nw")
        canvas.create_text(0.7*screen_width + root.deck_img.width()//2, 100+root.deck_img.height(),text=f"{len(g.players[1].deck)}", anchor="s", fill="white", font=("Times New Roman", 32, "bold"))
        
        #graveyard
        
        graveyard_cards = [[],[]]
        total_area = 0.7 * screen_width
        for i in range(2):
            for card in g.players[i].graveyard:
                if(card <= 0):
                    continue
                imgpath = f'./picture/cards/{card}.png'
                pil_img = Image.open(imgpath)
                factor = 1/6 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                if i == 1:
                    pil_img = pil_img.rotate(180)
                card_img = ImageTk.PhotoImage(pil_img)
                graveyard_cards[i].append(card_img)
        root.graveyard_cards = graveyard_cards
        
        
        if not hasattr(root, "graveyard_windows"):
            root.graveyard_windows = [None, None]
            for i in range(2):
                if root.graveyard_windows[i] is None or not root.graveyard_windows[i].winfo_exists():
                    root.graveyard_windows[i] = tkinter.Toplevel(root)
                    
                    root.graveyard_windows[i].title(f"player[{i}]'s graveyard")
                    root.graveyard_windows[i].geometry("800x600")
                    # Place the graveyard window at the bottom right of the screen
                    screen_w = root.winfo_screenwidth()
                    screen_h = root.winfo_screenheight()
                    win_w, win_h = 800, 600
                    x = screen_w - win_w
                    y = screen_h - win_h
                    if i == 0:
                        root.graveyard_windows[i].geometry(f"{win_w}x{win_h}+{x}+{y}")
                    else:
                        # Place player 1's graveyard window at the top right of the screen
                        root.graveyard_windows[i].geometry(f"{win_w}x{win_h}+{x}+0")
                        
                    root.graveyard_windows[i].resizable(False, False)
                    root.graveyard_windows[i].canvas = tkinter.Canvas(root.graveyard_windows[i], width=800, height=600, bg="#474646")
                    root.graveyard_windows[i].canvas.pack(fill="both", expand=True)
        for i in range(2):
            root.graveyard_windows[i].canvas.delete("all")
            # print(g.players[i].graveyard)
            for card in range(len(root.graveyard_cards[i])):
                try:
                    # print(card%10 * root.graveyard_cards[i][card].width(), card//10 * root.graveyard_cards[i][card].height())
                    root.graveyard_windows[i].canvas.create_image(card%10 * root.graveyard_cards[i][card].width(), card//10 * root.graveyard_cards[i][card].height(), image=root.graveyard_cards[i][card], anchor="nw")
                except:
                    pass
        if(len(g.players[0].graveyard)):
            try:
                canvas.create_image(0.7*screen_width + root.deck_img.width()+0.001*screen_width, screen_height-100, image=root.graveyard_cards[0][-1], anchor="sw")
                canvas.create_text(0.7*screen_width + root.deck_img.width()+0.001*screen_width + root.graveyard_cards[0][-1].width()//2, screen_height-100,text=f"{len(g.players[0].graveyard)}", anchor="s", fill="red", font=("Times New Roman", 32, "bold"))
            except:
                pass
        
        if(len(g.players[1].graveyard)):
            try:
                canvas.create_image(0.7*screen_width + root.deck_img.width()+0.001*screen_width, 100, image=root.graveyard_cards[1][-1], anchor="nw")
                canvas.create_text(0.7*screen_width + root.deck_img.width()+0.001*screen_width + root.graveyard_cards[0][-1].width()//2, 100+root.deck_img.height(),text=f"{len(g.players[1].graveyard)}", anchor="s", fill="red", font=("Times New Roman", 32, "bold"))
            except:
                pass
        
        
        # draw using card_space
        
        using_cards = [[],[]]
        total_area = 0.7 * screen_width
        for i in range(2):
            for card in g.players[i].usecards:
                if(card <= 0):
                    continue
                imgpath = f'./picture/cards/{card}.png'
                pil_img = Image.open(imgpath)
                factor = (total_area / len(g.players[i].usecards))/pil_img.width
                if (factor*pil_img.height) > 1/8 * screen_height:
                    factor = 1/8 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                if i == 1:
                    pil_img = pil_img.rotate(180)
                card_img = ImageTk.PhotoImage(pil_img)
                using_cards[i].append(card_img)
        root.using_cards = using_cards
        
        for i in range(len(g.players[0].usecards)):
            width = int(root.using_cards[0][0].width())
            try:
                canvas.create_image(i*width, screen_height-100-root.deck_img.height(), image=root.using_cards[0][i], anchor="sw")
            except:
                pass
        for i in range(len(g.players[1].usecards)):
            width = int(root.using_cards[1][0].width())
            try:
                canvas.create_image(i*width, 100+root.deck_img.height(), image=root.using_cards[1][i], anchor="nw")
            except:
                pass
        
        #twist
        
        twists_img = [[],[]]
        total_area = 0.1*screen_width
        for i in range(2):
            for card in g.players[i].metamorphosis:
                if(card <= 0):
                    continue
                imgpath = f'./picture/cards/{card}.png'
                pil_img = Image.open(imgpath)
                factor = (total_area / len(g.players[i].metamorphosis))/pil_img.width
                if (factor*pil_img.height) > 1/8 * screen_height:
                    factor = 1/8 * screen_height / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                if i == 1:
                    pil_img = pil_img.rotate(180)
                card_img = ImageTk.PhotoImage(pil_img)

                twists_img[i].append(card_img)
        root.twists_img = twists_img
        
        for i in range(len(g.players[0].metamorphosis)):
            try:
                canvas.create_image(0.7*screen_width + root.deck_img.width()*2 + 0.001 * screen_width + i*root.twists_img[0][i].width(), screen_height-100, image=root.twists_img[0][i], anchor = "sw")
            except:
                pass
        for i in range(len(g.players[1].metamorphosis)):
            try:
                canvas.create_image(0.7*screen_width + root.deck_img.width()*2 + 0.001 * screen_width + i*root.twists_img[1][i].width(), 100, image=root.twists_img[1][i], anchor = "nw")
            except:
                pass
        
        # character special
        for i in range(2):
            y = screen_height-100 if i == 0 else 0
            if g.players[i].identity.idx == 0:
                # print(g.players[i].identity.characterName)
                savecard = [None, None, None]
                for c in range(3):
                    if g.players[i].identity.saveCard[c] == -1:
                        continue
                    imgpath = f'./picture/cards/{g.players[i].identity.saveCard[c]}.png'
                    pil_img = Image.open(imgpath)
                    factor =100 / pil_img.height
                    pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                    if i == 1:
                        pil_img = pil_img.rotate(180)
                    card_img = ImageTk.PhotoImage(pil_img)

                    savecard[c] = card_img
                root.savecard = savecard
                for c in range(3):
                    if savecard[c] is not None:
                        canvas.create_image(750 + c*root.savecard[i].width(),y, image = root.savecard[c], anchor="nw") 
                pass
            elif g.players[i].identity.idx == 1:
                topPosion = None
                # print(g.players[i].identity.remindPosion)
                if len(g.players[i].identity.remindPosion) > 0:
                    imgpath = f'./picture/cards/{g.players[i].identity.remindPosion[0]}.png'
                    pil_img = Image.open(imgpath)
                    factor =100 / pil_img.height
                    pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                    if i == 1:
                        pil_img = pil_img.rotate(180)
                    topPosion = ImageTk.PhotoImage(pil_img)
                root.topPosion = topPosion
                if topPosion is not None:
                    canvas.create_image(750,y, image = root.topPosion, anchor="nw") 
                pass
            elif g.players[i].identity.idx == 2:
                canvas.create_image(750, y, image = root.awakenTK_img, anchor = "nw")
                canvas.create_text(900, y, text=f"{g.players[i].identity.AWAKEN_TOKEN}/6", anchor="nw", fill="black", font=("Times New Roman", 32))
                
                pass
            elif g.players[i].identity.idx == 3:
                if g.players[i].identity.identity == 1:
                    img_path = './picture/character/alice/queen_of_hearts.png'
                if g.players[i].identity.identity == 2:
                    img_path = './picture/character/alice/mad_hatter.png'
                if g.players[i].identity.identity == 3:
                    img_path = './picture/character/alice/cheshire_cat.png'
                    
                pil_img = Image.open(img_path)
                factor =100 / pil_img.height
                pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                    
                root.nowidentity = ImageTk.PhotoImage(pil_img)
                canvas.create_image(750, y, image = root.nowidentity, anchor = "nw")
                
                pass
            elif g.players[i].identity.idx == 4:
                canvas.create_image(750, y, image = root.QITK_img, anchor = "nw")
                canvas.create_text(900, y, text=f"{g.players[i].identity.KI_TOKEN}/12", anchor="nw", fill="black", font=("Times New Roman", 32))
                
                pass
            elif g.players[i].identity.idx == 5:
                
                pass
            elif g.players[i].identity.idx == 6:
                for loc in g.tentacle_TOKEN_locate:
                    canvas.create_image(10 + (loc)*fieldSize, screen_height//2 + 0.005*screen_height, image=root.tentacleTK_img, anchor="nw")
                pass
            elif g.players[i].identity.idx == 7:
                torch = None
                if g.players[i].identity.remindMatch > 0:
                    imgpath = f'./picture/cards/134.png'
                    pil_img = Image.open(imgpath)
                    factor =100 / pil_img.height
                    pil_img = pil_img.resize((int(factor*pil_img.width), int(factor*pil_img.height)), Image.Resampling.LANCZOS)
                    if i == 1:
                        pil_img = pil_img.rotate(180)
                    torch = ImageTk.PhotoImage(pil_img)
                root.remindtorch = torch
                if torch is not None:
                    canvas.create_image(750,y, image = root.remindtorch, anchor="nw") 
                pass
            elif g.players[i].identity.idx == 8:
                canvas.create_image(750, y, image = root.comboTK_img, anchor = "nw")
                canvas.create_text(900, y, text=f"{g.players[i].identity.COMBO_TOKEN}/12", anchor="nw", fill="black", font=("Times New Roman", 32))
                pass
            elif g.players[i].identity.idx == 9:
                for c, loc in enumerate(g.players[i].identity.destiny_TOKEN_locate):
                    color = g.players[i].identity.destiny_TOKEN_type[c]
                    if loc < 0:
                        sz = 100
                        for j in range(3):
                            if root.skill_img[1-i][j] is not None:
                                sz = root.skill_img[1-i][j].width()
                                break
                        putY = screen_height-100-root.deck_img.height() if i == 1 else 100+root.deck_img.height()
                        putX = 0.7*screen_width + ((-loc)-1)*sz
                    else:
                        width = 0.1 * screen_width / 3
                        row = (loc-1)//3
                        col = (loc-1) % 3
                        putX = 0.87*screen_width + col*width
                        putY = 0.3*screen_height + row*(0.3*screen_height/4)
                    if color == 1:
                        canvas.create_image(putX, putY, image=root.bluefateTK_img, anchor = "nw")
                    else:
                        canvas.create_image(putX, putY, image=root.redfateTK_img, anchor = "nw")
                        
                pass
            
            # if openGraveyard > 0:
                
    root.after(30, updateScreen, root, g)
def killScreen(root):
    root.destroy()