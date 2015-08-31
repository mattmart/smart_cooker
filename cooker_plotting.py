import plotly.plotly as py
import argparse
import pdb
import psycopg2
from plotly.graph_objs import *

class CookerPlotter:
    def _get_trace_data(self, uuid):
        self._conn=psycopg2.connect("dbname=cooker user=cooker")
        DEC2FLOAT = psycopg2.extensions.new_type(psycopg2.extensions.DECIMAL.values,'DEC2FLOAT',
                    lambda value, curs: float(value) if value is not None else None)

        psycopg2.extensions.register_type(DEC2FLOAT)

        self._curr = self._conn.cursor()
        self._curr.execute("select cooking_description from t_cooking_descriptions where uuid = '%s'" % uuid)
        _description = self._curr.fetchone()[0]

        self._curr.execute("select ts,curr_temp from t_sc_timing where uuid = '%s'" % uuid)
        x_axis = []
        y_axis = []

        for row in self._curr.fetchall():
            x_axis.append(row[0])
            y_axis.append(row[1])

        return Scatter(x=x_axis,y=y_axis,mode='lines'), _description

    def _get_unique_url(self, uuid):
        scatterplot, description = self._get_trace_data(uuid) 
        data = Data([scatterplot])
        
        layout = Layout(
            title= description,
            showlegend=True,
            autosize=True,
            xaxis = XAxis (
                title = "Time"
            ),
            yaxis = YAxis (
                title = "Temperature in Celsius"
            )
        )

        fig = Figure(data=data, layout=layout)
        unique_url = py.plot(fig, filename = uuid,auto_open=False)
        return unique_url

    def upload_to_plotly(self,uuid):
        return self._get_unique_url(uuid)


def main():
    plotter = CookerPlotter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--uuid", help="uuid to fetch from the database and graph", type=str)
    _myargs = parser.parse_args()
    
    print plotter.upload_to_plotly(_myargs.uuid)

if __name__ == "__main__":
    main()
