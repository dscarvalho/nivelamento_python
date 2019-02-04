import web
import random
import json
import numpy as np
from datetime import datetime

from ttt_model import TTTBoard, TTTPlayer, BSIZE, WIN, LOSE
        
urls = (
    '/ttt.*', 'TicTacToe'
)
app = web.application(urls, globals())

app.games = dict()
app.cpu_player = TTTPlayer()
app.cur_id = 0


class TicTacToe:        
    def GET(self):
        row = web.input(row=None)["row"]
        col = web.input(col=None)["col"]
        session_id = web.input(session=None)["session"]
        start = web.input(start=False)["start"]

        print(app.games)

        res = dict()
        if (bool(start)):
            player_num = random.choice([1,2])
            app.cur_id += 1
            app.games[app.cur_id] = {"board": TTTBoard(), "player_num": player_num}
            res["player_num"] = player_num
            res["session"] = app.cur_id

            if (player_num == 2):
                app.cpu_player.start_game(1)
                cpu_move = app.cpu_player.make_move(app.games[app.cur_id]["board"].board)
                res["cpu_move"] = cpu_move 
                app.games[app.cur_id]["board"].mark(cpu_move[0], cpu_move[1], 1)
            else:
                app.cpu_player.start_game(2)

            if (len(app.games) > 100):
                oldest_session, g = sorted(games.items(), key=lambda e: e[1]["starttime"])[0]
                del app.games[oldest_session]

            return json.dumps(res)
        else:
            game = None
            try:
                print("Session: ", session_id)
                session_id = int(session_id)
                res["session"] = session_id
                game = app.games[session_id]
                print("game: ", game)
                player_num = game["player_num"]
                cpu_player_num = 1 if (player_num == 2) else 2
            except(KeyError, TypeError):
                return json.dumps({"error": "Session non-existent or expired."})

            try:
                row = int(row)
                col = int(col)
            except:
                return json.dumps({"error": "Invalid move. Must be integers from 0 to %d ." % (BSIZE - 1)})


            if (not game["board"].mark(row, col, player_num)):
                return json.dumps({"error": "Invalid move. Position already occupied."})
            else:
                won = game["board"].checkwin()
                if (won):
                    res["end"] = True
                    res["winner"] = player_num
                    app.cpu_player.learn(LOSE)
                elif (game["board"].checkdraw()):
                    res["end"] = True
                    res["winner"] = 0
                else:
                    cpu_move = app.cpu_player.make_move(game["board"].board)
                    game["board"].mark(cpu_move[0], cpu_move[1], cpu_player_num)
                    res["row"] = cpu_move[0]
                    res["col"] = cpu_move[1]

                    won = game["board"].checkwin()

                    if (won):
                        res["end"] = True
                        res["winner"] = cpu_player_num
                        app.cpu_player.learn(WIN)

                if (game["board"].checkdraw()):
                    res["end"] = True
                    res["winner"] = 0


        return res





if __name__ == "__main__":
    app.run()
