import matplotlib.pyplot as plt
from matplotlib import patches


def get_transformed_radius(radius):
    ''' Formule qui retourne le nouveau rayon de la bulle après avoir été chauffée '''
    return 2*radius


radius = 1.0
transformed = get_transformed_radius(radius)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')

bulle_originale = patches.Circle((0.0, 0.0),
                                  radius=radius,
                                  color='b', alpha=0.5,
                                  fill=True, label='Bulle originale')

bulle_modif = patches.Circle((0.0, 0.0),
                             radius=transformed,
                             color='r',
                             alpha=0.5, fill=True,
                             label='Bulle chauffée')


ax1.add_patch(bulle_modif)
ax1.add_patch(bulle_originale)

ax1.autoscale_view()
plt.legend()
plt.show()