import plotly.plotly as py
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
        self._curr.execute("select ts,curr_temp from t_sc_timing where uuid = '%s'" % uuid)
        x_axis = []
        y_axis = []

        for row in self._curr.fetchall():
            x_axis.append(row[0])
            y_axis.append(row[1])

        return Scatter(x=x_axis,y=y_axis,mode='lines')

    def _get_unique_url(self, uuid):
        data = Data([self._get_trace_data(uuid)])
        
        layout = Layout(
            title= "test graph",
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
        unique_url = py.plot(fig, filename = 'basic-line',auto_open=False)
        return unique_url

    def upload_to_plotly(self,uuid):
        return self._get_unique_url(uuid)


def main():
    plotter = CookerPlotter()
    print plotter.upload_to_plotly('3df70992-e324-4eb8-9354-afe1f7ac5744')

if __name__ == "__main__":
    main()
