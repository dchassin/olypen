#!/usr/bin/perl
#
# name: clear.pl
# auth: DP Chassin
# date: 12/2005
# desc: Market clearing code
# note: Tables (fields) used:
#       * cust_meter_trans (demand, read_time)
#       * buy (quantity, price, posttime)
#       * sell (quantity, price, posttime)
#	* clear (posttime, quantity, price, avg24, std24, avg168, std168)
# bugs: 1) Database login/pwd is hardcoded
#
# hist: 2005-12-11: created (DP Chassin)
#       2005-12-15: added avg/std recording
#	2005-12-19: remove code that assumes meter load can be used for uncurtailable bid; uncurtailed load must bid so
#

use DBI;

$dbh = DBI->connect("DBI:mysql:olypen","olypen","power123");
$sth;

# get total meter
$sth = $dbh->prepare('SELECT SUM(demand) FROM cust_meter_trans WHERE read_time > date_sub(now(), interval 5 minute)')
	or die "Couldn't prepare query for total demand: " . $dbh->errstr;
$sth->execute() or die "Couldn't get total buy quantity: " . $sth->errstr;
$total_demand = $sth->fetchrow_array();

#print "\tTotal demand: $total_demand kW\n";

# get total buys
$sth = $dbh->prepare('SELECT SUM(quantity) FROM buy WHERE posttime > date_sub(now(), interval 5 minute)')
	or die "Couldn't prepare query for total buy: " . $dbh->errstr;
$sth->execute() or die "Couldn't get total buy quantity: " . $sth->errstr;
$total_buy = $sth->fetchrow_array();

#print "\tTotal buys: $total_buy kW\n";

# get buys
$sth = $dbh->prepare('SELECT quantity, price FROM buy WHERE posttime > date_sub(now(),interval 5 minute) ORDER BY price DESC') 
	or die "Couldn't prepare buy query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;

# build demand curve
$n_buyers=0;
while (@data = $sth->fetchrow_array()) {
	$buy_q[$n_buyers] = $buy_q[$n_buyers-1] + $data[0];
	$buy_p[$n_buyers] = $data[1];
	$n_buyers++;
}

#for (0..$n_buyers-1) {
#	print "\tbuyer $_: $buy_q[$_] kW for $buy_p[$_] USD/MWh\n";
#}

# get sells
$sth = $dbh->prepare('SELECT quantity, price FROM sell WHERE posttime > date_sub(now(), interval 5 minute) order by price ASC')
	or die "Couldn't prepare sell query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;

# build supply curve
$n_sellers=0;
while (@data = $sth->fetchrow_array()) {
	if ($n_sellers==0) {
		$sell_q[$n_sellers] = $data[0];
	}
	else {
		$sell_q[$n_sellers] = $sell_q[$n_sellers-1] + $data[0];
	}
	$sell_p[$n_sellers] = $data[1];
	$n_sellers++;
}

#for (0..$n_sellers-1) {
#	print "\tseller $_: $sell_q[$_] kW for $sell_p[$_] USD/MWh\n";
#}

$i=0;
$j=0;
$check=0;
while ($i<$n_buyers && $j<$n_sellers && $buy_p[$i] >= $sell_p[$j]) {
	if ($buy_q[$i] > $sell_q[$j]) {
		$clear_q = $sell_q[$j];
		$a = $b = $buy_p[$i];
		$j++;
		$check=0;
	}
	elsif ($buy_q[$i] < $sell_q[$j]) {
		$clear_q = $buy_q[$i];
		$a = $b = $sell_p[$j];
		$i++;
		$check=0;
	}
	else {
		$clear_q = $buy_q[$i];
		$a = $buy_p[$i];
		$b = $sell_p[$j];
		$i++; $j++;
		$check=1;
	}
}
while ($check==1) {
	if ($i>0 && $i<$n_buyers && ($a+$b)/2 <= $buy_p[$i]) {
		$b = $buy_p[$i];
		$i++;
	}
	elsif ($j>0 && $j<$n_sellers && ($a+$b)/2 <= $sell_p[$j]) {
		$a = $sell_p[$j];
		$j++;
	}
	else {
		$check = 0;
	}
}
$clear_p = ($a+$b)/2;

# make sure zero-load clear at price of first unit
if ($clear_q==0 && $n_sellers>0) {
	$clear_p = $sell_p[0];
}

# get 24 hours clear history
$sth = $dbh->prepare("SELECT avg(price), std(price) FROM clear WHERE posttime BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY) AND NOW() AND price < 9999")
	or die "Couldn't prepare clear history query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;
if (@data = $sth->fetchrow_array()) {
	$avg24 = $data[0];
	$std24 = $data[1];
}

# get 168 hours clear history
$sth = $dbh->prepare("SELECT avg(price), std(price) FROM clear WHERE posttime BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() AND price < 9999")
	or die "Couldn't prepare clear history query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;
if (@data = $sth->fetchrow_array()) {
	$avg168 = $data[0];
	$std168 = $data[1];
}

my($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst) = localtime;
$year+=1900;
$mon++;
printf 'INSERT INTO clear (posttime, mkt_id, quantity, price, avg24, std24, avg168, std168) VALUES ("%d-%d-%d %d:%d:00", floor(unix_timestamp(now())/300), %.3f, %.2f, %.2f, %.2f, %.2f, %.2f)', $year,$mon,$day,$hour,$min, $clear_q, $clear_p, $avg24, $std24, $avg168, $std168;
