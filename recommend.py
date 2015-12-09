import sys
import math

def createMatrix(filename):
	"""Return a dict with all the records.  Each record is a dictionary 
	containing the ratings"""
	
	data = {}
	averageRatings = {}
	counts = {}

	for line in open(filename):
		record = line.split()
		user = int(record[0])
		movie = int(record[1])
		rating = int(record[2])

		if user not in data:
			data[user] = {}
			averageRatings[user] = 0
			counts[user] = 0

		data[user][movie] = rating
		averageRatings[user] += rating
		counts[user] += 1

	# update the averageRatings
	for user in averageRatings:
		averageRatings[user] /= float(counts[user])

	return data, averageRatings

def computeItemSimilarities(maxId, ratings, averageRatings):
	"""Compute sim(i,j)"""

	sim = [[0 for y in range(maxId + 1)] for x in range(maxId + 1)]

	for i in range(1, maxId + 1):
		for j in range(1, maxId + 1):

			# skip if i and j are the same movies
			if i == j:
				sim[i][j] = 1
				continue
			
			top = left = right = 0

			for u in ratings:
				a = ratings[u].get(i, 0) - averageRatings[u]
				b = ratings[u].get(j, 0) - averageRatings[u]

				top += a * b
				left += a ** 2
				right += b ** 2 

			sim[i][j] = float(top) / (math.sqrt(left) * math.sqrt(right))
			print "(%d,%d) = %f" % (i,j,sim[i][j])

	return sim

def computeKSimilar(sim, k):
	"""gather the top k similar items for each item. Each entry is a list
	of tuples, each elemeent is (index, sim[i][j])"""

	lst = []

	for i in range(len(sim)):
		row = list(enumerate(sim[i]))
		row.pop(i)	# remove (i,i) entries
		tmp = sorted(row, key=lambda entry: entry[1], reverse=True)
		tmp = tmp[:k]
		lst.append(tmp)

	return lst

def predict(user, item, ksim, ratings):
	"""Predict the rating for (user, item) even if it is included"""

	top = 0
	bottom = 0

	for j, s in ksim[item]:
		print 'j', j
		top += ratings[user].get(j, 0) * s
		bottom += s
	
	return float(top) / bottom




if __name__ == '__main__':
	
	numberOfMovies = 4
	data, averageRatings = createMatrix('ratings.csv')

	print data 
	print averageRatings
	sim = computeItemSimilarities(numberOfMovies, data, averageRatings)
	print sim
	print
	ksim = computeKSimilar(sim, int(math.sqrt(numberOfMovies)))
	print 'rating for user1, movie 4', predict(2, 1, ksim, data)

