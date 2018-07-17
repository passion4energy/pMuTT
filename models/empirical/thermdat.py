
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import variation
from warnings import warn
from Thermochemistry import constants as c
from Thermochemistry.models.empirical import BaseThermo

class Thermdat(BaseThermo):
	"""
	Stores the information for an individual thermdat specie
	Inherits from Thermochemistry.models.empirical.BaseThermo

	The thermodynamic properties are calculated using the following form:
	Cp/R = a[0] + a[1]*T + a[2]*T^2 + a[3]*T^3+a[4]*T^4
	H/RT = a[0] + a[1]*T/2 + a[2]*T^2/3 + a[3]*T^3/4 + a[4]*T^4/5 + a[5]/T
	S/R = a[0]*ln(T) + a[1]*T + a[2]*T^2/2 + a[3]*T^3/3 + a[4]*T^4/4 + a[6]

	Attributes
		T_low - float
			Lower temperature bound (in K)
		T_mid - float
			Middle temperature bound (in K)
		T_high - float
			High temperature bound (in K)
		a_low - (7,) ndarray
			NASA polynomial to use between T_low and T_mid
		a_high - (7,) ndarray
			NASA polynomial to use between T_mid and T_high
	"""
	def __init__(self, T_low=None, T_mid=None, T_high=None, a_low=np.zeros(7), a_high=np.zeros(7), **kwargs):
		super().__init__(**kwargs)
		self.T_low = T_low
		self.T_mid = T_mid
		self.T_high = T_high
		self.a_low = a_low
		self.a_high = a_high

	def get_a(self, T):
		"""
		Returns the correct polynomial range based on T_low, T_mid and T_high

		Parameters
			T - float
				Temperature in K
		Returns
			(7,) ndarray
				NASA polynomial coefficients
		"""
		if T < self.T_mid:
			if T < self.T_low:
				warn('Temperature below T_low for {}'.format(self.name), RuntimeWarning)
			return self.a_low
		else:
			if T > self.T_high:
				warn('Temperature above T_high for {}'.format(self.name), RuntimeWarning)
			return self.a_high

	def get_CpoR(self, Ts):
		"""
		Calculate the dimensionless heat capacity

		Parameters
			Ts - float or (N,) ndarray
				Temperature(s) in K
		Returns
			float or (N,) ndarray
				Dimensionless heat capacity
		"""
		try:
			iter(Ts)
		except TypeError:
			a = self.get_a(T=Ts)
			CpoR = get_nasa_CpoR(a=a, T=Ts)
		else:
			CpoR = np.zeros(len(Ts))
			for i, T in enumerate(Ts):
				a = self.get_a(T)
				CpoR[i] = get_nasa_CpoR(a=a, T=T)
		return CpoR

	def get_HoRT(self, Ts):
		"""
		Calculate the dimensionless enthalpy

		Parameters
			Ts - float or (N,) ndarray
				Temperature(s) in K
		Returns
			float or (N,) ndarray
				Dimensionless heat capacity		
		"""
		try:
			iter(Ts)
		except TypeError:
			a = self.get_a(T=Ts)
			HoRT = get_nasa_HoRT(a=a, T=Ts)
		else:
			HoRT = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				a = self.get_a(T=T)
				HoRT[i] = get_nasa_HoRT(a=a,T=T)
		return HoRT

	def get_SoR(self, Ts):
		"""
		Calculate the dimensionless entropy

		Parameters
			Ts - float or (N,) ndarray
				Temperature(s) in K
		Returns
			float or (N,) ndarray
				Dimensionless entropy		
		"""
		try:
			iter(Ts)
		except TypeError:
			a = self.get_a(T=Ts)
			SoR = get_nasa_SoR(a=a,T=Ts)
		else:
			SoR = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				a = self.get_a(T=T)
				SoR[i] = get_nasa_SoR(a=a, T=T)
		return SoR

	def get_GoRT(self, Ts):
		"""
		Calculate the dimensionless entropy

		Parameters
			Ts - float or (N,) ndarray
				Temperature(s) in K
		Returns
			float or (N,) ndarray
				Dimensionless Gibbs energy		
		"""
		try:
			iter(Ts)
		except TypeError:
			a = self.get_a(T=Ts)
			GoRT = get_nasa_GoRT(a=a, T=Ts)
		else:
			GoRT = np.zeros_like(Ts)
			for i, T in enumerate(Ts):
				a = self.get_a(T=T)
				GoRT[i] = get_nasa_GoRT(a=a, T=T)
		return GoRT

	def calc_nasa(self, T_low=None, T_high=None, Ts=None, CpoR=None, T_ref=None, HoRT_ref=None, SoR_ref=None):
		"""
		Calculates the NASA polynomials using internal attributes

		Parameters
			T_low - float
				Lower temperature to fit. If not specified, uses T_low attribute
			T_high - float
				High temperature to fit. If not specified, uses T_high attribute
			Ts - (N,) ndarray
				Temperatures in K used for fitting CpoR. If not specified, calculates using self.get_CpoR
			CpoR - (N,) ndarray
				Dimensionless heat capacity corresponding to T
			T_ref - float
				Reference temperature in K used for fitting HoRT_ref and SoR_ref. If not specified, uses T_ref attribute
			HoRT_ref - float
				Dimensionless enthalpy that corresponds to T_ref. If not specified, uses HoRT_ref attribute.
				If the HoRT_ref attribute is not specified, uses self.get_HoRT
			SoR_ref - float
				Dimensionless entropy that corresponds to T_ref. If not specified, uses self.get_SoR
		"""

		'''
		Processing inputs
		'''
		#Get lower temperature bound
		if T_low is None:
			T_low = self.T_low
		else:
			self.T_low = T_low

		#Get higher temperature bound
		if T_high is None:
			T_high = self.T_high
		else:
			self.T_high = T_high
		
		#Get temperatures
		if Ts is None:
			Ts = np.linspace(T_low, T_high)

		#Get heat capacity data
		if CpoR is None:
			CpoR = self.thermo_model.get_CpoR(Ts=Ts)

		#Get reference temperature
		if T_ref is None:
			T_ref = self.T_ref

		#Get reference enthalpy
		if HoRT_ref is None:
			if self.HoRT_ref is None:
				HoRT_ref = self.thermo_model.get_HoRT(T=T_ref)
			else:
				HoRT_ref = self.HoRT_ref

		#Get reference entropy
		if SoR_ref is None:
			SoR_ref = self.thermo_model.get_SoR(Ts=T_ref)

		#Reinitialize coefficients
		self.a_low = np.zeros(7)
		self.a_high = np.zeros(7)

		'''
		Processing data
		'''
		self.fit_CpoR(Ts=Ts, CpoR=CpoR)
		self.fit_HoRT(T_ref=T_ref, HoRT_ref=HoRT_ref)
		self.fit_SoR(T_ref=T_ref, SoR_ref=SoR_ref)

	def fit_CpoR(self, Ts, CpoR):
		"""
		Fit a[0]-a[4] coefficients in a_low and a_high attributes given the dimensionless heat capacity data

		Parameters
			Ts - (N,) ndarray
				Temperatures in K
			CpoR - (N,) ndarray
				Dimensionless heat capacity
		"""
		#If the Cp/R does not vary with temperature (occurs when no vibrational frequencies are listed)
		if (np.mean(CpoR) < 1e-6 and np.isnan(variation(CpoR))) or variation(CpoR) < 1e-3 or all(np.isnan(CpoR)):
		   self.T_mid = Ts[int(len(Ts)/2)]
		   self.a_low = np.zeros(7)
		   self.a_high = np.zeros(7)
		else:
			max_R2 = -1
			R2 = np.zero_like(Ts)
			for i, T_mid in enumerate(Ts):
				#Need at least 5 points to fit the polynomial
				if i > 5 and i < (len(Ts)-6):
					#Separate the temperature and heat capacities into low and high range
					(R2[i], a_low, a_high) = self._get_CpoR_R2(Ts=Ts, CpoR=CpoR, i_mid=i)
			max_R2 = max(R2)
			max_i = np.where(max_R2 == R2)[0][0]
			(max_R2, a_low_rev, a_high_rev) = self._get_CpoR_R2(Ts=Ts, CpoR=CpoR, i_mid=max_i)
			empty_arr = np.zeros(2)
			self.T_mid = Ts[max_i]
			self.a_low = np.concatenate((a_low_rev[::-1], empty_arr))
			self.a_high = np.concatenate((a_high_rev[::-1], empty_arr))

	def _get_CpoR_R2(self, Ts, CpoR, i_mid):
		"""
		Calculates the R2 polynomial regression value.
		Parameters
			Ts - (N,) ndarray
				Temperatures (K) to fit the polynomial
			CpoR - (N,) ndarray
				Dimensionless heat capacities that correspond to T array
			i_mid - int
				Index that splits T and CpoR arrays into a lower and higher range
		Returns
			R2 - float
				R2 value resulting from NASA polynomial fit to T and CpoR
			p_low - (5,) ndarray
				Polynomial corresponding to lower range of data
			p_high - (5,) ndarray
				Polynomial corresponding to high range of data
		"""
		T_low = Ts[:i_mid]
		CpoR_low = CpoR[:i_mid]
		T_high = Ts[i_mid:]
		CpoR_high = CpoR[i_mid:]
		#Fit the polynomial
		p_low = np.polyfit(x = T_low, y = CpoR_low, deg = 4)
		p_high = np.polyfit(x = T_high, y = CpoR_high, deg = 4)

		#Find the R2
		CpoR_low_fit = np.polyval(p_low, T_low)
		CpoR_high_fit = np.polyval(p_high, T_high)
		CpoR_fit = np.concatenate((CpoR_low_fit, CpoR_high_fit))
		CpoR_mean = np.mean(CpoR)
		ss_reg = np.sum((CpoR_fit - CpoR_mean)**2)
		ss_tot = np.sum((CpoR - CpoR_mean)**2)
		R2 = ss_reg / ss_tot

		return (R2, p_low, p_high)

	def fit_HoRT(self, T_ref, HoRT_ref):
		"""
		Fit a[5] coefficient in a_low and a_high attributes given the dimensionless enthalpy

		Parameters
			T_ref - float
				Reference temperature in K
			HoRT_ref - float
				Reference dimensionless enthalpy
		"""
		T_mid = self.T_mid
		a6_low = (HoRT_ref - get_nasa_HoRT(a=self.a_low, T=T_ref))*T_ref
		a6_high = (HoRT_ref - get_nasa_HoRT(a=self.a_high, T=T_ref))*T_ref

		#Correcting for offset
		H_low_last_T = get_nasa_HoRT(a=self.a_low, T=T_mid) + a6_low/T_mid
		H_high_first_T = get_nasa_HoRT(a=self.a_high, T=T_mid) + a6_high/T_mid
		H_offset = H_low_last_T - H_high_first_T

		self.a_low[5] = a6_low
		self.a_high[5] = T_mid * (a6_high/T_mid + H_offset)

	def fit_SoR(self, T_ref, SoR_ref):
		"""
		Fit a[6] coefficient in a_low and a_high attributes given the dimensionless entropy

		Parameters
			T_ref - float
				Reference temperature in K
			SoR_ref - float
				Reference dimensionless entropy
		"""
		T_mid = self.T_mid
		a7_low = SoR_ref - get_nasa_SoR(a=self.a_low, T=T_ref)
		a7_high = SoR_ref - get_nasa_SoR(a=self.a_high, T=T_ref)

		#Correcting for offset
		S_low_last_T = get_nasa_SoR(a=self.a_low, T=T_mid) + a7_low
		S_high_first_T = get_nasa_SoR(a=self.a_high, T=T_mid) + a7_high
		S_offset = S_low_last_T - S_high_first_T

		self.a_low[6] = a7_low
		self.a_high[6] = a7_high + S_offset

def get_nasa_CpoR(a, T):
	"""
	Calculates the dimensionless heat capacity using NASA polynomial form

	Parameters
		a - (7,) ndarray
			Coefficients of NASA polynomial
		T - float
			Temperature in K

	Returns
		float
			Dimensionless heat capacity
	"""
	T_arr = np.array([1., T, T**2, T**3, T**4, 0., 0.])
	return np.dot(a, T_arr)

def get_nasa_HoRT(a, T):
	"""
	Calculates the dimensionless enthalpy using NASA polynomial form

	Parameters
		a - (7,) ndarray
			Coefficients of NASA polynomial
		T - float
			Temperature in K

	Returns
		float
			Dimensionless enthalpy
	"""
	T_arr = np.array([1., T/2., T**2/3, T**3/4, T**4/5, 1./T, 0.])
	return np.dot(a, T_arr)

def get_nasa_SoR(a, T):
	"""
	Calculates the dimensionless entropy using NASA polynomial form

	Parameters
		a - (7,) ndarray
			Coefficients of NASA polynomial
		T - float
			Temperature in K

	Returns
		float
			Dimensionless entropy
	"""
	T_arr = np.array([np.log(T), T, T**2/2, T**3/3, T**4/4, 0., 1.])
	return np.dot(a, T_arr)

def get_nasa_GoRT(a, T):
	"""
	Calculates the dimensionless Gibbs free energy using NASA polynomial form

	Parameters
		a - (7,) ndarray
			Coefficients of NASA polynomial
		T - float
			Temperature in K

	Returns
		float
			Dimensionless entropy
	"""
	return get_nasa_HoRT(a=a, T=T)-get_nasa_SoR(a=a, T=T)
