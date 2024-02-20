jobData = {'Customer Name': 'Greg', 'Job Name': 'Testing Post-form Stuff ', 'Kitchen Depth': 10.0, 'Kitchen Depth Deck': 0.0, 'Vanity Depth': 0.0, 'Vanity Depth Deck': 0.0, '12" Bar': 0.0, '15" Bar': 0.0, '18" Bar': 0.0, '26" Bar': 5.0, '27" Bar': 0.0, '32" Bar': 0.0, '36" Bar': 0.0, '42" Bar': 0.0, '45" Bar': 0.0}

colorsToPrice = []
stockedOptions = {'Kitchen Depth': ["7732-58","7022-58","4551-60"], '12" Bar': ["7022-58"], '26" Bar': ['7732-58']}
lnftKeys = [key for key,value in jobData.items() if value and key not in ["Customer Name","Job Name"]]

print(lnftKeys)
for key in lnftKeys:
  if key not in stockedOptions.keys():
    print('found nonstocked option')
    colorsToPrice = []
    break #because is there is any non-stocked option then we can't stock pricing
  else:
    print('hello')

    if not colorsToPrice:
      colorsToPrice = stockedOptions[key]
    else:
      for color in colorsToPrice:
        if color not in stockedOptions[key]:
          colorsToPrice.remove(color)


print(colorsToPrice)
