import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os, shutil

def clipping(x, l, h):
    return np.maximum( l, np.minimum( x, h ) )

def sample_from_real(num_people, real_coords, real_data, lims):

    l_lon, h_lon, l_lat, h_lat = lims

    pop = np.array([ x[1] for x in real_data ])
    percs = pop / np.sum(pop)
    samples = (percs * num_people).astype("int32")
    mask = samples == 0

    masked_coords = np.array([ real_coords[i,:] for i in range(len(mask)) if mask[i] ])
    masked_data = [real_data[i] for i in range(len(mask)) if mask[i]]
    masked_pop = pop[mask]

    masked_percs = masked_pop / np.sum(masked_pop)
    masked_samples = (masked_percs * num_people).astype("int32")

    p_pos = []
    for i in range(len(masked_coords)):
        for j in range(masked_samples[i]):
            p_pos.append(masked_coords[i,:])
    p_pos = np.array(p_pos)

    lon_std = np.std(real_coords[:,1])
    lat_std = np.std(real_coords[:,0])

    print(lat_std, lon_std)

    p_pos[:,0] += ((np.random.rand(p_pos.shape[0]) - 0.5) / 5) * lat_std
    p_pos[:,1] += ((np.random.rand(p_pos.shape[0]) - 0.5) / 5) * lon_std
    print(p_pos)

    return p_pos, p_pos.shape[0], masked_coords, masked_data

def create_connections(p_pos, max_cluster_size, max_dist):

    assigned_clusters = np.arange(p_pos.shape[0])
    direct_connections = np.ones((p_pos.shape[0], ), dtype="int32") * -1
    connection_count = np.ones((p_pos.shape[0], ), dtype="int32")
    assigned_map = np.zeros((p_pos.shape[0], ), dtype="int32")

    for idx, pos in enumerate(p_pos):
        if connection_count[idx] >= max_cluster_size: continue
        dists = np.sum((p_pos - pos) ** 2, axis=1)
        close_list = np.argsort(dists)
        for p in close_list:
            if dists[p] > max_dist: break
            total_size = connection_count[p] + connection_count[idx]
            if total_size < max_cluster_size and assigned_clusters[idx] != assigned_clusters[p]: # uzaklık sınırı da ekle
                assigned_clusters[ assigned_clusters == assigned_clusters[idx] ] = assigned_clusters[p]
                connection_count[  assigned_clusters == assigned_clusters[idx] ] = total_size
                direct_connections[idx] = p
                break
            
    #print(len(np.unique(assigned_clusters)))
    #print(direct_connections)

    return direct_connections, assigned_clusters

def sample_from_random_seeds(num_people, num_seed, dist_ratio):
    seeds_count = np.round((np.random.dirichlet(np.ones(num_seed),size=1) * num_people)).astype("int32")[0,:]

    seeds = np.zeros((num_seed,2))
    seeds[:,0] = np.random.rand(num_seed)
    seeds[:,1] = np.random.rand(num_seed)

    p_pos = []
    for i in range(len(seeds_count)):
        for _ in range(seeds_count[i]):
            p_pos.append(seeds[i,:])
    p_pos = np.array(p_pos)
    num_people = np.sum(seeds_count)

    p_pos += ( np.random.rand(num_people, 2) - 0.5 ) * 2 * dist_ratio

    return p_pos, num_people

    

if __name__ == "__main__":

    # parameters
    DIR = "anim/"
    momentum = 0.9
    distraction = 0.4
    step_scaler = 0.01
    num_people = 500
    num_centroids = 15
    max_cluster_size = 15
    num_seed = 20
    dist_ratio = 0.1

    p_pos, num_people = sample_from_random_seeds(num_people, num_seed, dist_ratio)

    #p_pos = np.zeros((num_people,2))
    #p_pos[:,0] = np.random.rand(num_people)
    #p_pos[:,1] = np.random.rand(num_people)

    p_vel = (np.random.rand(num_people,2) - 0.5) * step_scaler

    centroids = np.zeros((num_centroids,2))
    centroids[:,0] = np.random.uniform(0.1,0.9,num_centroids)
    centroids[:,1] = np.random.uniform(0.1,0.9,num_centroids)

    """
    centroids = np.array([ [0.15, 0.15],
                           [0.15, 0.5],
                           [0.15, 0.85],
                           [0.5, 0.15],
                           [0.5, 0.5],
                           [0.5, 0.85],
                           [0.85, 0.15],
                           [0.85, 0.5],
                           [0.85, 0.85]])
    num_centroids = len(centroids)
    centroids += (np.random.rand(num_centroids, 2) - 0.5) * 0.1
    """

    cmap = plt.get_cmap('RdYlGn')
    #colors = cmap(np.linspace(0, 1, len(author_set)))

    signal_strength = np.random.rand(num_people)

    # Vectorized code piece to find closest centroids
    outer_subs = np.subtract.outer(p_pos, centroids)
    x_dist = outer_subs[:,0,:,0]
    y_dist = outer_subs[:,1,:,1]
    dist_matrix = x_dist ** 2 + y_dist ** 2
    closest_centroids = np.argmin(dist_matrix, axis=1)

    # For calculation purposes create a matrix with assigned centroids
    assigned_centroids = centroids[closest_centroids, :]

    shutil.rmtree(DIR)
    os.makedirs(DIR)

    ims = []

    for i in range(400):

        connections, assigned_clusters = create_connections(p_pos, max_cluster_size, 0.01)

        hosts_map = np.zeros((num_people,), dtype="uint8")

        for c in np.unique(assigned_clusters):
            group = np.arange(num_people)[assigned_clusters == c]
            max_signal = -1
            max_idx = -1
            for p in group:
                if signal_strength[p] > max_signal:
                    max_idx = p
                    max_signal = signal_strength[p]
            hosts_map[max_idx] = 1


        
        for idx, pos in enumerate(p_pos):
            if hosts_map[idx]:
                plt.plot(pos[0], pos[1], marker="o", color="blue", MarkerSize=2)
            else:
                plt.plot(pos[0], pos[1], marker="o", color=cmap(signal_strength[idx]), MarkerSize=1)

        plt.plot(centroids[:,0], centroids[:,1], "r+", MarkerSize=3)

        plt.axis('off')
        plt.axis('equal')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        if i == 0:
             plt.savefig(DIR + "main" + ".png", dpi=200, bbox_inches='tight', pad_inches=0)

        p_new_vel = (np.random.rand(num_people,2) - 0.5) * step_scaler
        p_direct_vel = ( assigned_centroids - p_pos - (np.random.rand(num_people,2) - 0.5) * step_scaler ) * step_scaler
        p_vel = momentum * p_vel + (1 - momentum) * ( distraction * p_new_vel + (1 - distraction) * p_direct_vel)

        p_pos += p_vel
        p_pos[:, 0] = clipping(p_pos[:, 0], 0, 1)
        p_pos[:, 1] = clipping(p_pos[:, 1], 0, 1)

        signal_strength += (np.random.rand(num_people) - 0.5) * 2 * 0.1
        signal_strength = clipping(signal_strength, 0, 1)

        for idx, p in enumerate(connections):
            if p != -1:
                plt.plot( [p_pos[idx,0], p_pos[p, 0]], [p_pos[idx,1], p_pos[p, 1]], "black", linewidth=0.3)

        plt.axis('off')
        plt.axis('equal')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.savefig(DIR + str(i) + ".png", dpi=200, bbox_inches='tight', pad_inches=0)
        plt.clf()
        plt.close()
