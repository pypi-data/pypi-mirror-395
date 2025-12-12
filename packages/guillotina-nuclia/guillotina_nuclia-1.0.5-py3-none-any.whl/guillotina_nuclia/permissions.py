from guillotina import configure


configure.permission("nuclia.Predict", "Allow to predict")
configure.permission("nuclia.Ask", "Allow to ask")
configure.permission("nuclia.Search", "Allow to search")
configure.permission("nuclia.Find", "Allow to find")
configure.grant(role="guillotina.Manager", permission="nuclia.Predict")
configure.grant(role="guillotina.Manager", permission="nuclia.Ask")
configure.grant(role="guillotina.Manager", permission="nuclia.Search")
configure.grant(role="guillotina.Manager", permission="nuclia.Find")
