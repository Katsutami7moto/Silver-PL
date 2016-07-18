int fibonacci (int x )
{
if ((x >= 0) && (x < 2))
{
return x;
}
else
{
return (fibonacci((x - 1)) + fibonacci((x - 2)));
}
}
int n;
scanf("%d", &n);
int x = 1;
int y = 0;
int ans = 0;
int i = 1;
while (i <= n)
{
ans = (x + y);
x = y;
y = ans;
i = (i + 1);
}
printf("%d\n", ans);
