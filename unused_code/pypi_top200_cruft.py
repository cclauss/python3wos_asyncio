import scene

ui = scene.ui

# pip_loc is a tuple of lists of tuples.  Use tuples where possible because
# lists require slightly more RAM.  For each domino die from 0 to 9 there is a
# list of the coordinates of the dots/pips.
pip_locs = ([()],
            [(1,1)],
            [(0,0), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,0), (2,0), (0,2), (2,2)],
            [(0,0), (0,2), (1,1), (2,0), (2,2)],
            [(0,0), (1,0), (2,0), (0,2), (1,2), (2,2)],
            [(0,0), (1,0), (2,0), (1,1), (0,2), (1,2), (2,2)],
            [(0,0), (1,0), (2,0), (0,1), (2,1), (0,2), (1,2), (2,2)],
            [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)])


def generateDominosYield(inMaxDie = 6):  # Yield = Generator -- is an iterator
    for x in range(inMaxDie + 1):
        for y in range(inMaxDie + 1):
            if not x > y:
                yield (x, y)

def domino_image(pips=(5, 6), width=600, fg_color='blue', bg_color='grey'):
    height = int(width / 2)
    with ui.ImageContext(width, height) as ctx:
        # domino is rounded rect in background color
        ui.set_color(bg_color)
        ui.Path.rounded_rect(0, 0, width, height, height / 10).fill()
        # pips are circles in foreground color
        ui.set_color(fg_color)
        pip_size = height / 3
        b = int(height / 18)
        wh = pip_size - 2 * b
        # draw pips[0]
        for loc in pip_locs[pips[0]]:
            if loc:
                x, y = loc
                ui.Path.oval(x * pip_size + b, y * pip_size + b, wh, wh).fill()
        # draw dividing line
        path = ui.Path()
        path.line_width = 4
        path.move_to(height, b)
        path.line_to(height, height - b)
        path.close()
        path.stroke()
        # draw pips[1]
        for loc in pip_locs[pips[1]]:
            if loc:
                x, y = loc
                ui.Path.oval(x * pip_size + b + height, y * pip_size + b, wh, wh).fill()
        return scene.Texture(ctx.get_image())
        

class MyScene(scene.Scene):
    def old_setup(self):
        domino = self.make_domino()

    def setup(self):
        hud_up(0)
        bufferSize = 4
        maxDie = 6
        # print(1)
        dieSize = int((self.bounds.w - bufferSize * 6) / 14)
        print('dieSize', dieSize)
        top = int((self.bounds.h - bufferSize * 6) / 7)
        print('top', top)
        # print(2)
        
        w = dieSize * 2
        h = dieSize
        #for i in range(7):
            #for j in range(7):
                #if not i > j:
        hud_up(3)
        for (i, j) in generateDominosYield(maxDie):
            hud_up(0)
            theDomino = DominoNode((i, j), dieSize)
            sys.exit(7)
            theDomino.frame.x = j * (w + bufferSize)
            theDomino.frame.y = top + i * (h + bufferSize)
            #theDomino.rotation = 90
            
            #self.add_layer(theDomino)
            self.add_child(theDomino)
            print(theDomino)

    def make_domino(self):
        return scene.SpriteNode(domino_image(pips=(5, 6)), parent=self,
                                position=self.bounds.center())

if __name__ == '__main__':
    scene.run(MyScene(), show_fps=False)
