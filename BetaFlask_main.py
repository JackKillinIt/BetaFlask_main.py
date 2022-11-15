# import random so we can use random numbers
import random
import secrets

# Import flask which is a micro web framework written in Python.
from flask import (
    Flask,
    jsonify, render_template, session, Response
)

import BetaController
# Function that create the app
import GraphController
import LabData

# matplot lib gives us the ability to draw charts

'''
create_app will be called when we want to start listening on a port for http traffic. It's main purpose is to rerun a flask object with routes (URLS) defined

'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    '''
    Update this function to correctly call the functions to generate the data.
    Keep the variables the same
    '''

    @app.route('/Beta/<stockName>/<numberOfPeriods>')
    def Beta(stockName="AAPL", numberOfPeriods=10):
        numberOfPeriods = int(numberOfPeriods)
        base_betas = [1]
        chunked_betas = [2]

        ############
        # Uncomment below and replace the function call below with the call to BetaController's do_calculations function, passing stockName and number of Periods)
        base_betas, chunked_betas = BetaController.do_calculations(stockName, numberOfPeriods)
        ############

        session["stock_name"] = stockName
        session['beta_list'] = chunked_betas
        session['base_line_list'] = base_betas
        session['numberOfPeriods'] = numberOfPeriods
        return render_template('hello_world.html', stockName=stockName)

    @app.route('/beta/plot.png')
    def plot_png():
        beta_list = session['beta_list']
        base_line_list = session['base_line_list']
        stockName = session["stock_name"]
        #### Debug statement
        print("In Flask's plot_png Debug: Going to create a chart with the following values", "beta list: ", beta_list,
              "base_line: ",
              base_line_list, "Security Name:", stockName, sep='\n')
        #####
        # once you have completed the output assignment below this below line can be commented out
        # output = GraphController.create_figure(stockName)

        ########
        # Reset the output function below.
        output = GraphController.draw_beta_chart_with_baseline(beta_list, base_line_list, stockName)
        ########
        return Response(output.getvalue(), mimetype='image/png')

    #  Simple route
    @app.route('/')
    def hello_world():
        return jsonify({
            "status": "success",
            "message": "Hello World, you need to goto /Beta/APPL/10 for this project!"
        })

    '''
    EVERYTHING IN THE FOLLOWING ROUTE WAS ALL WRITTEN BY ME (JACK) AND SHOULD SATISFY ALL THE REQUIREMENTS FOR THE 
    MIDTERM ASSIGNMENT :D. The only thing that could cause issue is the vague try, except statement. In my time playing
    with my program, the broadness of the except statement did not give rise to any issues, so there should be nothing 
    to worry about. The try portion creates a json file with the name of the stock and the beta output in your browser,
    the except portion handles cases (such as betaREST/FB/10) where stockName (FB, the ticker) is invalid, and produces
    an outfile writing in the name of the invalid stock and the number of periods the user inputted, along with 
    writing the same message into a json file that appears in the user's browser.
    '''

    @app.route('/betaREST/<stockName>/<numberOfPeriods>')  # Declaring route
    def beta_rest(stockName, numberOfPeriods):
        try:
            numberOfPeriods = int(numberOfPeriods)
            output = BetaController.do_calculations(stockName, numberOfPeriods)  # Obtains beta values
            returnValue = jsonify({"Ticker": stockName, "Data": output})
            # return jsonify({"Ticker": stockName, "Data": output})  # Outputs JSON file with data
        except:  # If stock name is not in LabData.py
            outfile = open("BadData.txt", "w")  # Opens a new writing file
            outfile.write(str({"ticker": stockName, "numberOfChunks": numberOfPeriods}))  # Adds params to new file
            outfile.write("\n")
            outfile.close()
            returnValue = jsonify({"ticker": stockName, "number of chunks": numberOfPeriods})
            # return jsonify({"ticker": stockName, "number of chunks": numberOfPeriods})  # Returns json of invalid data
        return returnValue

    return app  # do not forget to return the app


APP = create_app()

if __name__ == '__main__':
    ranGuess = random.randint(2, 100)
    port = 8081
    url_to_test = "http://127.0.0.1:" + str(port) + "/Beta/AAPL/" + str(ranGuess)
    print("goto ", url_to_test, " to test")
    APP.run(debug=True, port=8081)
