INSERT INTO foo.t1 SELECT
    number, 
    now() - randUniform(1, 1000000.),
    
    15 + round(randExponential(1 / 10), 2)
FROM numbers(100);

SELECT sleep(3);

INSERT INTO foo.t1 SELECT
    number, 
    now() - randUniform(1, 1000000.),
    
    15 + round(randExponential(1 / 10), 2)
FROM numbers(100);

SELECT sleep(3);

INSERT INTO foo.t1 SELECT
    number, 
    now() - randUniform(1, 1000000.),
    
    15 + round(randExponential(1 / 10), 2)
FROM numbers(100);

SELECT sleep(3);


INSERT INTO foo.t2 SELECT
    number, 
    now() - randUniform(1, 1000000.),
    
    15 + round(randExponential(1 / 10), 2)
FROM numbers(100);