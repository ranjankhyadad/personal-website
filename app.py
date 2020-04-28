from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/stock-analysis/")
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import show, output_file, figure
    #for getting web components
    from bokeh.embed import components 
    from bokeh.resources import CDN

    start = datetime.datetime(2019,12,1)
    end = datetime.datetime(2020,4,1)

    df = data.DataReader(name = "GOOG",data_source = "yahoo", start = start, end = end)

    def status(c,o):
        if c>o:
            status = "Increase"
        elif c<o:
            status = "Decrease"
        else:
            status = "Unchanged"
        return status

    df["Status"] = [ status(c,o) for c,o in zip(df["Close"], df["Open"])]

    df["Centre"] = (df.Open+df.Close)/2

    fig = figure(title = "Analysis", x_axis_type="datetime", height=300, width =1000, sizing_mode ="scale_width")
    fig.grid.grid_line_alpha = 0.4

    #layer1
    #segment parameters - segment(xval of highest point, yval of highest point, 
    #                     xval of lowest. yval of lowest)
    fig.segment(df.index, df.High, df.index, df.Low, color ="Grey")

    #layer2
    #parameters for rect- [x-axis, y-axis(centre),width, height]
    # here width =12 hrs = 12*60*60*1000= 43200000 ms
    fig.rect(df.index[df["Status"]=="Increase"], df.Centre[df["Status"]=="Increase"], 
            43200000, abs(df.Close-df.Open), fill_color="#98FB98", line_color ="black" )
    fig.rect(df.index[df["Status"]=="Decrease"], df.Centre[df["Status"]=="Decrease"], 
            43200000, abs(df.Close-df.Open), fill_color="red", line_color ="black")

    script, div = components(fig)
    # cdn_css = CDN.css_files ---> CSS files are discontinued. Hence, no need to use css files on webpage
    cdn_js = CDN.js_files[0]

    return render_template("plot.html", script= script, div= div, cdn_js=cdn_js)

if __name__ == "__main__":
    app.run(debug=True)