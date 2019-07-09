# ------------
# load the data
using DataFrames
using DataFramesMeta
using CSV

path = "data/events.csv";
rawd = DataFrame(CSV.File(path));
data = dropmissing(rawd[2:4]);
data[:eventscore] = map(x -> x == "view" ? 1 : x == "addtocart" ? 2 : 3, data[:event]);

byvi = by(data, [:visitorid, :itemid], x -> DataFrame(score = sum(x[:eventscore])));
byvi = byvi[byvi[:score] .!= 0, :];
sort!(byvi, :visitorid)

user = sort(unique(byvi[:visitorid]));
item = sort(unique(byvi[:itemid]));

rows = byvi[:visitorid];
cols = byvi[:itemid];
vals = byvi[:score];

sparse(rows, cols, vals)