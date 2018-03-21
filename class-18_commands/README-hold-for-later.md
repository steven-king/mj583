# Output the clean wiki data

Run the notebook server from class 10

```
docker run -p 9000:9000 -d -t steventking/data-viz:pandas-cleaning
```

Go to 127.0.0.1:9000 and export the cleaned data to JSON. See
`Cleaning Wiki Dates & Save To JSON.ipynb`

The export command should be:

```
df.to_json("wiki-clean.json", orient="records")
```

The 2nd argument is the "orientation" of the output data. By using the `records`
format we will get a list containing each record instead of a mapping of columns
and their data.

Consider a dataframe with the following contents:

```
d = pd.DataFrame([{"col_a":"some value", "col_b":"another value"}])
```

Which looks like:

```
        col_a          col_b
0  some value  another value
```

Now compare the default orientation with the `records` orientation:

```
print(d.to_json())

>>> {"col_a":{"0":"some value"},"col_b":{"0":"another value"}}

print(d.to_json(orient="records"))
>>> [{"col_a":"some value","col_b":"another value"}]
```

Go to the home page of the notebook server and download the JSON.

--------------------------------------------------------------------------------
