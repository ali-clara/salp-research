function dr = model(r,m,k,b,f)

dr(1,1) = r(2);
dr(2,1) = (-k/m)*r(1) + (-b/m)*r(2) + (1/m)*f;