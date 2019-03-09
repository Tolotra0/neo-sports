from flask import Blueprint, jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


clustering_api = Blueprint('clustering_api', __name__)
