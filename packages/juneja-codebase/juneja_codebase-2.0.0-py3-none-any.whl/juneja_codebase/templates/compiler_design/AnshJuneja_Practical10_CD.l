%{
#include "y.tab.h"
%}

%%

[a-z]      { return LETTER; }
[0-9]      { return DIGIT; }
\n         { return '\n'; }

.          { return -1; }

%%

int yywrap() { return 1; }
