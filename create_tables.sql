CREATE TABLE `executions` (
  `execution_id` int NOT NULL AUTO_INCREMENT,
  `inserted` int DEFAULT NULL,
  `exec_time_items` time DEFAULT NULL,
  `exec_time_details` time DEFAULT NULL,
  `dateproc` varchar(45) DEFAULT NULL,
  `exec_timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`execution_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=ascii;

CREATE TABLE `items` (
  `id` varchar(45) DEFAULT NULL,
  `seller_id` varchar(45) DEFAULT NULL,
  `warranty` varchar(50) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `sold_quantity` int DEFAULT NULL,
  `usd_price` float DEFAULT NULL,
  `logistic_type` varchar(45) DEFAULT NULL,
  `condition` varchar(45) DEFAULT NULL,
  `execution_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='        df = pd.DataFrame(columns=[''id'', ''seller_id'', ''warranty'', ''price'', ''sold_quantity'', ''usd_price'', ''logistic_type''])\n';
