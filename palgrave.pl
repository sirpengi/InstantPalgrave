print "what's your name?\n";
my $name = <STDIN>;
$name =~ s/\n//;
print "hello $name!\nhope you're having a nice day.\n";
