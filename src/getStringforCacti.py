def makeStrinng(readings):
    st = ""
    for key,value in readings.items():
	if value['temp'] == None:
            st = st + 'temp' + str(key) + ':' + '0.0' + ' '
        else:
            st = st + 'temp' + str(key) + ':' + str(value['temp']) + ' '

        if value['humid'] == None or value['humid'] > 100 or value['humid'] < 0:
            st = st + 'humid' + str(key) + ':' + '0.0' + ' '
        else:
            st = st + 'humid' + str(key) + ':' + str(value['humid']) + ' '

    print st.strip()
