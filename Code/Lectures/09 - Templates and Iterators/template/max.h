

template <typename T>
class Max_Min
{
public :

	T
	Max(T a, T b)
	{
		return (a > b) ? a : b;
	}
	T Min(T a, T b)
	{
		return (a < b) ? a : b;
	}
};

template <typename T1, typename T2>
void Print(T1 a, T2 b)
{
	std::cout << a << " " << b << std::endl;
}
