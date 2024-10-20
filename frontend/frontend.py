from make_back_request import make_request
import pandas as pd
import streamlit as st
st.title("Live Chess Player Ratings")
st.subheader("♟️ Esse site tem o objetivo de mostrar informações de rating atualizada dos melhores jogadores de xadrez do mundo! ♟️")
data = make_request()
if data:
    df = pd.DataFrame(data["message"])
    st.dataframe(df, hide_index=True)