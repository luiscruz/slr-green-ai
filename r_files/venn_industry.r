library(eulerr)
authorship <-  euler(c(Academic = 76, Industrial = 3, "Academic&Industrial" = 21),  shape = "ellipse")
plot(authorship,  quantities =list(fontfamily = "Linux Libertine", fontsize=24), labels = list(fontfamily = "Linux Libertine", fontsize=24))