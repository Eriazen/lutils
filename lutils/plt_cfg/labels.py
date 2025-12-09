

class Labels:
    '''
    Stores preset plot labels.
    '''

    def __init__(self):
        self._velocity = {'title': 'Velocity profile',
                          'xlabel': '$y$ / $-$', 'ylabel': '$U_x$ / $m \\cdot s^{-1}$'}
        self._k = {'title': 'Turbulence kinetic energy profile',
                   'xlabel': '$y$ / $-$', 'ylabel': '$k$ / $m^{2} \\cdot s^{-2}$'}
        self._nut = {'title': 'Turbulence viscosity profile',
                     'xlabel': '$y$ / $-$', 'ylabel': '$\\nu_t$ / $m^{2} \\cdot s^{-1}$'}
        self._epsilon = {'title': 'Turbulence dissipation profile',
                         'xlabel': '$y$ / $-$', 'ylabel': '$\\varepsilon$ / $m^{2} \\cdot s^{-3}$'}
        self._omega = {'title': 'Specific trubulence dissipation rate profile',
                       'xlabel': '$y$ / $-$', 'ylabel': '$\\omega$ / s^{-1}$'}

    @property
    def velocity(self) -> dict[str, str]:
        return self._velocity

    @property
    def k(self):
        return self._k

    @property
    def nut(self):
        return self._nut

    @property
    def epsilon(self):
        return self._epsilon

    @property
    def omega(self):
        return self._omega
