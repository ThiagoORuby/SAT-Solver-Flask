from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from dpll.SATSolver import dpll
from pkg.pysat import solver
from pkg.pysat import branch_heuristics as solvers

def create_app():

    app = Flask(__name__)



    @app.route("/", methods=['GET', 'POST'])
    def index():
        print_list = []
        column_list = []
        value_list = []
        result = ''
        method = ''
        if request.method == 'POST':
            kb = request.form['kb']
            method = request.form['method']
            #print(kb)
            if method == "Classic_DPLL":
                l = kb.splitlines()
                #print(l)
                result, print_list, column_list, value_list = dpll(kb)
            elif method == 'Chaff_Similar':
                l = list(set(kb))
                literals = [(l[i], i+1) for i in range(len(l)) if l[i].isnumeric()]
                print(literals)
                firstline = "p cnf {} {}".format(len(literals), len(kb.splitlines()))
                lista = [i.replace("!", "-") + ' 0\n' for i in kb.splitlines()]
                print(firstline)
                print(lista)
                with open('input.cnf', 'w') as f:
                    f.write(firstline + '\n')
                    f.writelines(lista)
                # Pysat
                solver = getattr(solvers, 'DynamicLargestIndividualSumSolver')('input.cnf')
                result, _, _, print_list, table_list = solver.run()
                result = "SATISFIABLE" if result else "UNSATISFIABLE"
                column_list = table_list[0].keys()
                value_list = [i.values() for i in table_list]
        return render_template('index.html', print_list = print_list, column_list = column_list, value_list = value_list, result = result, method = method)
    
    @app.route('/about')
    def about():
        return render_template('about.html')

    return app
