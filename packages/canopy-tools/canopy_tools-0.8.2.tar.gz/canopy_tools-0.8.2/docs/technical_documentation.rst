.. _technical_documentation:

Technical Documentation
=======================

.. _lonlat_gridops:

Spatial Reduction Operations on the 'lonlat' grid
-------------------------------------------------

The ``lonlat`` grid describes a geographic grid. Coordinates are longitude (:math:`\lambda`) and latitude (:math:`\phi`), and the angular spacing between gridpoints is constant (although it can be different for each axis).

Let :math:`F(\lambda, \phi, t)` be a field and :math:`M(\lambda, \phi)` a *gridlist mask*, defined by:

.. math::

    M(\lambda, \phi) =
    \begin{cases}
    1\text{ if } (\lambda, \phi) \text{ is a gridlist point;}\\
    0\text{ if } (\lambda, \phi) \text{ is not a gridlist point.}
    \end{cases}

For example, lakes and oceans are typically excluded from LPJ-GUESS gridlists, so the value of the mask at those points is :math:`0`. In the formulae below, coordinates are in radians, and :math:`R_\oplus` is the radius of Earth in :math:`\mathrm{m}`. In this system, the area of a gridcell is :math:`A(\lambda,\phi)=R_\oplus^2 \Delta\lambda\Delta\phi\cos(\phi)`.

Latitudinal Average
^^^^^^^^^^^^^^^^^^^

.. math::

    \mathrm{Av}_\phi(\lambda,t) = \frac{\sum_\phi F(\lambda, \phi, t) M(\lambda, \phi)}{\sum_\phi M(\lambda, \phi)}

Longitudinal Average
^^^^^^^^^^^^^^^^^^^^

.. math::

    \mathrm{Av}_\lambda(\phi,t) = \frac{\sum_\lambda F(\lambda, \phi, t) M(\lambda, \phi)}{\sum_\lambda M(\lambda, \phi)}

Spatial Average
^^^^^^^^^^^^^^^

.. math::

    \mathrm{Av}_{\lambda,\phi}(t) = \frac{\sum_{\lambda,\phi} F(\lambda, \phi, t) M(\lambda, \phi) \cos(\lambda)}{\sum_{\lambda,\phi} M(\lambda, \phi) \cos(\lambda)}

Longitudinal Sum
^^^^^^^^^^^^^^^^

.. math::

    \mathrm{Sum}_\lambda(\phi,t) = R_\oplus \Delta\lambda \cos\phi \sum_\lambda F(\lambda, \phi, t) M(\lambda, \phi)

Latitudinal Sum
^^^^^^^^^^^^^^^

.. math::

    \mathrm{Sum}_\phi(\lambda,t) = R_\oplus \Delta\phi \sum_\phi F(\lambda, \phi, t) M(\lambda, \phi)

Spatial Sum
^^^^^^^^^^^

.. math::

    \mathrm{Sum}_{\lambda,\phi}(t) = R_\oplus^2 \Delta\lambda\Delta\phi \sum_{\lambda,\phi} F(\lambda, \phi, t) M(\lambda, \phi) \cos(\phi)
