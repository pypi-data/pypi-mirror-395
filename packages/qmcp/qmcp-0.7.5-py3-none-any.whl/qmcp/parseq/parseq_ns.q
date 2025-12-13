.parseq.f: asc `abs`cor`ej`gtime`like`mins`prev`scov`system`wavg`acos`cos`ema`hclose`lj`ljf`mmax`prior`sdev`tables`where`aj`aj0`count`enlist`hcount`load`mmin`rand`select`tan`while`ajf`ajf0`cov`eval`hdel`log`mmu`rank`set`til`within`all`cross`except`hopen`lower`mod`ratios`setenv`trim`wj`wj1`and`csv`exec`hsym`lsq`msum`raze`show`type`wsum`any`cut`exit`iasc`ltime`neg`read0`signum`uj`ujf`xasc`asc`delete`exp`idesc`ltrim`next`read1`sin`ungroup`xbar`asin`deltas`fby`if`mavg`not`reciprocal`sqrt`union`xcol`asof`desc`fills`ij`ijf`max`null`reval`ss`update`xcols`atan`dev`first`in`maxs`or`reverse`ssr`upper`xdesc`attr`differ`fkeys`insert`mcount`over`rload`string`upsert`xexp`avg`distinct`flip`inter`md5`parse`rotate`sublist`value`xgroup`avgs`div`floor`inv`mdev`peach`rsave`sum`var`xkey`bin`binr`do`get`key`med`pj`rtrim`sums`view`xlog`ceiling`dsave`getenv`keys`meta`prd`save`sv`views`xprev`cols`each`group`last`min`prds`scan`svar`vs`xrank`ww;
.parseq.t:{@[{type parse string x};x;`$"Not a function"]} each .parseq.f!.parseq.f; 
.parseq.x: ([] f:key .parseq.t; h:{$[-5h=type x;x;0]}each value .parseq.t);
.parseq.x: update p: (parse string@) each f from .parseq.x where h<>0;
.parseq.revDict: (.parseq.x`p)!string (.parseq.x`f);
.parseq.glyphs: asc "~`!@#$%^&*()-=+\":'/?.>,<";
.parseq.types: string ``Bool`Guid``Byte`Short`Int`Long`Real`Float`Char`Symbol`Timestamp`Month`Date`Datetime`Timespan`Minute`Second`Time;
.parseq.isOnlyGlyphs: {all {any x in .parseq.glyphs} each x};
.parseq.sstring: {$[type[x]=10h;x;string x]};
.parseq.paren:{[s;p] p,s,("([{"!")]}")p};
.parseq.parenl:{[l;p;sep] .parseq.paren[sep sv l;p]};
.parseq.ltrim2:{((x in " \n\r\t")?0b)_x};
.parseq.rtrim2: {neg[((reverse x in " \n\r\t")?0b)]_x};
.parseq.trim2: .parseq.rtrim2 .parseq.ltrim2 @;
.parseq.extractBody:{[funcStr]
    body: .parseq.trim2 1_-1_ .parseq.trim2 funcStr;
    if["["=first body;
      body:.parseq.trim2 (1+first ss[body;"]"])_body];
    body
    };
.parseq.func2string:{t: type x; revX: .parseq.revDict x; 
    $[
        .parseq.isOnlyGlyphs .parseq.sstring x; "Builtin",.parseq.paren[.parseq.sstring x;"["]; 
        count[revX]>0; "Builtin",.parseq.paren[revX;"["];
        t=100h; "Lambda",.parseq.paren[.parseq.func100string x;"["];
        string x]};
.parseq.func100string:{v: value x; .parseq.parenl[string v[1]; "["; ", "], ", ", .parseq.var2string parse .parseq.extractBody last v};
.parseq.var2string: {[x] t: type[x]; if[t>=100h; :.parseq.func2string[x];]; 
    if[t=99h; :"{",(.parseq.var2string[key x]),": ",(.parseq.var2string[value x]),"}";];
    at: abs t; $[t=0; "[",(", " sv .parseq.var2string each x),"]"; t>0;"L",.parseq.types[t],"[",(", " sv .parseq.sstring each x),"]";.parseq.types[neg t],"[",.parseq.sstring[x],"]"]};
.parseq.parseq: {.parseq.var2string parse x};