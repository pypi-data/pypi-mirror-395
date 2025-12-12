def strip_whitespaces(df):
    def stripper(x):
        if x and isinstance(x, str):
            return x.strip()
        else:
            return x

    df.rename(columns=stripper, inplace=True)
    df = df.map(stripper)

    return df
