def exp_model(x, y, expo=[0.7, 2], slope=[5, 10], intercept=[0, 30], sigma0=20):
    """
    likelihood function is y = intercept + slope * exp( x * exponent)
    :param x: datapoints
    :param y:  data
    :param expo:  exponent [mu and sigma]
    :param slope:
    :param intercept:
    :param sigma0: the variation of the result
    :return:  returns the model to fit_mc() and list of model parameter names as strings and model function
    """
    print('Exponential fit \n args: intercept, slope, expo')

    import pymc3 as pm
    import numpy as np

    with pm.Model() as exp_m:  # or exp_model = pm.Model()
        # model y ~ theta_1* exp(theta_2*x) + theta_3

        # Intercept  - theta_3
        intercept = pm.Normal('intercept', mu=intercept[0], sd=intercept[1])
        # Slope   - theta_2
        slope = pm.Normal('slope', mu=slope[0], sd=slope[1])
        # Exponent  - theta_1
        expo = pm.Normal('expo', mu=expo[0], sd=expo[1])
        # Estimate of mean
        mean = slope * np.exp(expo * x) + intercept

        # Standard deviation
        sigma = pm.HalfNormal('sigma', sd=sigma0)
        # Observed values
        Y_obs = pm.Normal('Y_obs', mu=mean, sd=sigma, observed=y)

    varnames = ['intercept', 'slope', 'expo']

    modelfun = lambda x1, y1: x1[0] + x1[1] * np.exp(x1[2] * y1)  # y is data
    return exp_m, varnames, modelfun


# noinspection PyIncorrectDocstring
def poly_model(x, y, order, intercept=[0, 20], sigma0=30, **kwargs):
    """
    models any polynomial
    **kwargs allows any number of key word arguments
    The polynomial function is intercept + a1*x + a2*x**2 + a3*x**3 + ...
    Order N of the polynomial gives the last aN multiplier
    :param x: datapoints
    :param y: data
    :param order: order of the polynomial  0, 1, 2, ...
    :param intercept:  the constant [mu, sigma] - mu is center point, sigma is deviation in normal distribution
    :param a1: first order multiplier [mu, sigma]
    :param a2: second order multiplier [mu, sigma]
    ...
    :param aN: Nth order multiplier [mu, sigma]
    :return: returns the model to fit_mc()  and list of model parameter names as strings and model function
    """

    import pymc3 as pm
    from .utils import poly_fun

    args = []
    argvals = []
    for oi in range(1, order + 1):
        aN = 'a' + str(oi)
        args.append(aN)
        isinargs = next((value for key, value in kwargs.items() if key == aN), None)
        if not isinargs:
            argvals.append([0, 30 / oi**4])
            exec('%s = [%f, %f]'%(aN, argvals[-1][0], argvals[-1][1]))
        else:
            argvals.append(isinargs)
        # print(aN, '=', argvals[-1])

    if order == 1:
        print('1st-order polynomial fit \n args: intercept,', args)
    elif order == 0:
        print('Constant fit')
    elif order == 2:
        print('2nd-order polynomial fit \n args: intercept', args)
    else:
        print('%dth-order polynomial fit \n args: intercept,'%order, args)

    with pm.Model() as poly_m:  # or exp_model = pm.Model()
        # model y ~ a1*x + a2*x**2 + a3*x**3 +.. + intercept

        # Intercept  - theta_3
        intercept = pm.Normal('intercept', mu=intercept[0], sd=intercept[1])
        mean = intercept
        varnames = ['intercept']
        # modelfun0 = lambda x1, y1: poly_fun(x, y, 0)  # y is data
        if order>0:
            a1 = pm.Normal('a1', mu=argvals[0][0], sd=argvals[0][1])
            mean += a1*x
            varnames.append('a1')
        if order>1:
            a2 = pm.Normal('a2', mu=argvals[1][0], sd=argvals[1][1])
            mean += a2 * x**2
            varnames.append('a2')
        if order > 2:
            a3 = pm.Normal('a3', mu=argvals[2][0], sd=argvals[2][1])
            mean += a3 * x**3
            varnames.append('a3')
        oi = 3
        while order > oi:

            exec('%s = pm.Normal("a%d", mu=argvals[oi][0], sd=argvals[oi][1])'%(args[oi], oi + 1))
            varnames.append('a%d'%(oi+1))

            mean += eval('%s*x**%d' % (args[oi], oi+1))

            oi += 1

        # Standard deviation
        sigma = pm.HalfNormal('sigma', sd=sigma0)
        # Observed values
        Y_obs = pm.Normal('Y_obs', mu=mean, sd=sigma, observed=y)

    modelfun = poly_fun  
    return poly_m, varnames, modelfun