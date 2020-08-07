#Select all review from two last days
SELECT * FROM yelp.review where review_time >= DATE_ADD(CURDATE(), INTERVAL -2 DAY);

#Select review has most review count
Select * from review order by review desc limit 1;

#Select 10 categories have much review count
Select * from category as cate
	join (Select res.category_id, sum(review.reviews) as reviews from restaurant as res 
		join (Select restaurant_id, sum(review) as reviews from review group by restaurant_id) as review 
		on res.id = review.restaurant_id
		group by res.category_id) as rv
	on rv.category_id = cate.id
    order by rv.reviews desc limit 10;
    
#Select funny, usefull, cool review of the restaurant
Select * from restaurant as res 
	join (Select restaurant_id, sum(funny) as funny, sum(cool) as cool, sum(usefull) as usefull from review where review.restaurant_id = 3 
		 group by review.restaurant_id) as review
	on res.id = review.restaurant_id
         
            