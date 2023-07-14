#!/usr/bin/perl
#
# name: cleard.pl
# auth: DP Chassin
# date: 12/2005
# desc: Debug version of market clearing code
# note: Tables (fields) used:
#       * cust_meter_trans (demand, read_time)
#       * buy (quantity, price, posttime)
#       * sell (quantity, price, posttime)
#	* clear (posttime, quantity, price, avg24, std24, avg168, std168)
# bugs: 1) Database login/pwd is hardcoded
#
# hist: 2005-12-11: created (DP Chassin)
#       2005-12-15: added avg/std reporting
#

use DBI;

print 'Date and time (yyyy-mm-dd hh:mm): [now] ';
chomp($cleartime=<STDIN>);
if ($cleartime=='') {
	$cleartime='now()';
}
else {
	$cleartime="'$cleartime'";
}

$dbh = DBI->connect("DBI:mysql:olypen","olypen","power123");
$sth;

# get total meter
$sth = $dbh->prepare("SELECT SUM(demand) FROM cust_meter_trans WHERE read_time BETWEEN DATE_SUB($cleartime, INTERVAL 5 MINUTE) AND $cleartime")
	or die "Couldn't prepare query for total demand: " . $dbh->errstr;
$sth->execute() or die "Couldn't get total buy quantity: " . $sth->errstr;
$total_demand = $sth->fetchrow_array();

print "\tTotal demand: $total_demand kW\n";

# get total buys
$sth = $dbh->prepare("SELECT SUM(quantity) FROM buy WHERE posttime BETWEEN DATE_SUB($cleartime, INTERVAL 5 MINUTE) AND $cleartime")
	or die "Couldn't prepare query for total buy: " . $dbh->errstr;
$sth->execute() or die "Couldn't get total buy quantity: " . $sth->errstr;
$total_buy = $sth->fetchrow_array();

print "\tTotal buys: $total_buy kW\n";

# get buys
$sth = $dbh->prepare("SELECT quantity, price FROM buy WHERE posttime BETWEEN DATE_SUB($cleartime, INTERVAL 5 MINUTE) AND $cleartime ORDER BY price DESC") 
	or die "Couldn't prepare buy query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;

# build demand curve
#$buy_q[0]=$total_demand - $total_buy;
#$buy_p[0]=9999;
#$buyer_id=1;
$buyer_id=0;
while (@data = $sth->fetchrow_array()) {
	$buy_q[$buyer_id] = $buy_q[$buyer_id-1] + $data[0];
	$buy_p[$buyer_id] = $data[1];
	$buyer_id++;
}

for (0..$buyer_id-1) {
	print "\tbuyer $_: $buy_q[$_] kW for $buy_p[$_] USD/MWh\n";
}

# get sells
$sth = $dbh->prepare("SELECT quantity, price FROM sell WHERE posttime BETWEEN DATE_SUB($cleartime, INTERVAL 5 MINUTE) AND $cleartime ORDER BY price ASC")
	or die "Couldn't prepare sell query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;

# build supply curve
$seller_id=0;
while (@data = $sth->fetchrow_array()) {
	if ($seller_id==0) {
		$sell_q[$seller_id] = $data[0];
	}
	else {
		$sell_q[$seller_id] = $sell_q[$seller_id-1] + $data[0];
	}
	$sell_p[$seller_id] = $data[1];
	$seller_id++;
}

for (0..$seller_id-1) {
	print "\tseller $_: $sell_q[$_] kW for $sell_p[$_] USD/MWh\n";
}

$i=0;
$j=0;
$check=0;
while ($i<$buyer_id && $j<$seller_id && $buy_p[$i] >= $sell_p[$j]) {
	print "DEBUG: buy_q[$i]=$buy_q[$i], buy_p[$i]=$buy_p[$i], sell_q[$j]=$sell_q[$j], sell_p[$j]=$sell_p[$j]\n";
	if ($buy_q[$i] > $sell_q[$j]) {
		$clear_q = $sell_q[$j];
		$a = $b = $buy_p[$i];
		$j++;
		print "DEBUG: marginal seller\n";
		$check=0;
	}
	elsif ($buy_q[$i] < $sell_q[$j]) {
		$clear_q = $buy_q[$i];
		$a = $b = $sell_p[$j];
		$i++;
		print "DEBUG: marginal buyer\n";
		$check=0;
	}
	else {
		$clear_q = $buy_q[$i];
		$a = $buy_p[$i];
		$b = $sell_p[$j];
		$i++; $j++;
		print "DEBUG: matched quantities\n";
		$check=1;
	}
}
while ($check==1) {
	if ($i>0 && $i<$buyer_id && ($a+$b)/2 <= $buy_p[$i]) {
		printf "DEBUG: inframarginal buyer at %.2f\n", ($a+$b)/2;
		$b = $buy_p[$i];
		$i++;
	}
	elsif ($j>0 && $j<$seller_id && ($a+$b)/2 <= $sell_p[$j]) {
		printf "DEBUG: inframarginal seller at %.2f\n", ($a+$b)/2;
		$a = $sell_p[$j];
		$j++;
	}
	else {
		$check = 0;
	}
}
$clear_p = ($a+$b)/2;

printf "Clear %.3f kW at %.2f USD/MWh\n", $clear_q, $clear_p;

# get 24 hours clear history
$sth = $dbh->prepare("SELECT avg(price), std(price) FROM clear WHERE posttime BETWEEN DATE_SUB($cleartime, INTERVAL 24 hour) AND $cleartime")
	or die "Couldn't prepare clear history query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;
if (@data = $sth->fetchrow_array()) {
	printf "1 day average price %.2f USD/MWh, stdev %.2f USD/MWh\n", $data[0], $data[1];
}

# get 168 hours clear history
$sth = $dbh->prepare("SELECT avg(price), std(price) FROM clear WHERE posttime BETWEEN DATE_SUB($cleartime, INTERVAL 168 hour) AND $cleartime")
	or die "Couldn't prepare clear history query: " . $dbh->errstr;
$sth->execute() or die "Couldn't execute query: " . $sth->errstr;
if (@data = $sth->fetchrow_array()) {
	printf "1 week average price %.2f USD/MWh, stdev %.2f USD/MWh\n", $data[0], $data[1];
}
