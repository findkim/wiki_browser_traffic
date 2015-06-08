library(ggplot2)
library(zoo)
d = read.csv("input.csv")
summary(d)
ggplot(d$user,d$url)
d$time = as.Date(d$dtg)
p <- ggplot(d[d$user=='aglahe',], aes(x=dtg, y=url, group=user, label=user))
p + geom_line() + geom_point()

for (i in d$user){
  p <- ggplot(d[d$user==i,], aes(x=dtg, y=url, group=user, label=user)) + geom_line() + geom_point()
  ggsave(plot = p,filename = paste(i,".jpg",sep=""),dpi=300)
}

firstday = read.csv("2015-04-13-memexwiki.csv")
p <- ggplot(firstday[d$user=='mgroh',], aes(x=time, y=url, group=user, label=user))
p + geom_line() + geom_point()

p <- ggplot(d, aes(x=dtg, y=url, group=user, label=user))
p + geom_line(aes(color=d$user)) + geom_point()

p + geom_line()
p + scale_x_date() 
p + geom_text(aes(color=d$user))
p + geom_text(size=3)
p + geom_point()
