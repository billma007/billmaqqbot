def race(length):
	members = ["🦈","🐙","🥜","🦃","👻"]
	who_is_win = [False,False,False,False,False]
	output = ""
	for i in range(5):
		if length[i] >= 19:
			length[i] = 19
			who_is_win[i] = True
		else:
			who_is_win[i] = False
		output += "{}:".format(i+1)+"="*(19-int(length[i]))+members[i]+"="*int(length[i])+"\n"
	return output,who_is_win



if __name__=="__main__":
    print(race([234,234,234,22123,123,123143,134234,2432424,2424342,34234324324,324243243,423423423,43243243243244,42341243132,2134134234213423412,234241324])[0])