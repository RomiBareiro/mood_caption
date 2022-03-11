import math

class Haversine:
    """Haversine is an aproximate method to get distances using
    GPS coordinates
    """
    def calculations(self, coord2, ref_lat, ref_long):
        """Use the haversine class to calculate the distance between
        two lon/lat coordnate pairs.
        output distance available in kilometers
        """
        lon2,lat2=coord2.split(" ")
        lon2 = float(lon2)
        lat2 = float(lat2)
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(ref_lat)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-ref_lat)
        delta_lambda=math.radians(lon2-ref_long)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=R*c                         
        return (self.meters/1000.0)            # output distance in kilometers
